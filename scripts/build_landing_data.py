"""Generate landing/metrics.json and landing/chunks.json for the
TaskTorrent public landing page.

Reads consumers.yaml, then for each registered consumer queries GitHub
for chunk-task issues and walks `_contribution_meta.yaml` files in the
consumer's contributions tree to aggregate metrics.

Privacy: contributor counts are aggregate-only. No usernames are
emitted to the landing page (per locked plan §4).

Run locally:
    GH_TOKEN=ghp_... python scripts/build_landing_data.py

In CI:
    Uses GITHUB_TOKEN provided by Actions. Same gh CLI binary.

Outputs:
    landing/metrics.json — totals + per-consumer breakdown + last_updated
    landing/chunks.json  — flat list of currently-claimable chunks across
                           all registered consumers, with metadata for
                           the landing page table.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONSUMERS_FILE = REPO_ROOT / "consumers.yaml"
LANDING_DIR = REPO_ROOT / "landing"

# Default token estimate per Drop, per docs/drop-system.md
TOKENS_PER_DROP = 100_000


# ---------- gh helpers ----------

def gh_api(path: str, fields: list[str] | None = None) -> object:
    """Call `gh api <path>` and parse JSON. Returns parsed value or [] / {} on failure."""
    cmd = ["gh", "api", path]
    if fields:
        cmd.extend(["--jq", "."])
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False,
                         encoding="utf-8", errors="replace")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if res.returncode != 0:
        print(f"WARN: gh api {path} failed: {res.stderr.strip()[:200]}", file=sys.stderr)
        return None
    try:
        return json.loads(res.stdout) if res.stdout.strip() else None
    except json.JSONDecodeError:
        return None


def gh_paginated(path: str) -> list:
    """Fetch all pages from a paginated GitHub API endpoint via gh CLI.

    `gh api --paginate` concatenates JSON arrays back-to-back: `[...][...]`.
    A naive `re.split(r"\\]\\s*\\[", text)` split is unsafe because issue
    bodies often contain Markdown checkboxes like `- [ ]\\n- [ ]` whose
    `]\\n[` substring also matches the page-boundary pattern. Instead we
    walk the string with a depth counter that respects JSON string escapes,
    and yield each top-level array as a complete unit.
    """
    cmd = ["gh", "api", "--paginate", path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False,
                             encoding="utf-8", errors="replace")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    if res.returncode != 0:
        print(f"WARN: gh api --paginate {path} failed: {res.stderr.strip()[:200]}", file=sys.stderr)
        return []
    text = res.stdout.strip()
    if not text:
        return []
    if not text.startswith("["):
        # Single object response, not an array — try a direct parse.
        try:
            obj = json.loads(text)
            return obj if isinstance(obj, list) else []
        except json.JSONDecodeError:
            return []

    out: list = []
    depth = 0
    in_string = False
    escape = False
    start = 0
    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if in_string:
            if ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "[":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                try:
                    arr = json.loads(text[start:i + 1])
                    if isinstance(arr, list):
                        out.extend(arr)
                except json.JSONDecodeError:
                    pass
    return out


def gh_raw_file(repo: str, path: str, ref: str = "HEAD") -> str | None:
    """Fetch raw file content from a GitHub repo via gh api."""
    api_path = f"repos/{repo}/contents/{path}?ref={ref}"
    res = gh_api(api_path)
    if not isinstance(res, dict) or "content" not in res:
        return None
    import base64
    try:
        return base64.b64decode(res["content"]).decode("utf-8", errors="replace")
    except Exception:
        return None


# ---------- Issue parsing ----------

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
DROPS_NUM_RE = re.compile(r"~?(\d+(?:\.\d+)?)\s*Drops?", re.IGNORECASE)


def _section_body(body: str, heading: str) -> str:
    matches = list(SECTION_RE.finditer(body))
    for i, m in enumerate(matches):
        if m.group(1).strip().lower() == heading.lower():
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            return body[start:end].strip()
    return ""


def _first_code(text: str) -> str | None:
    m = INLINE_CODE_RE.search(text)
    return m.group(1).strip() if m else None


def _drops_estimate(body: str) -> float | None:
    de = _section_body(body, "Drop Estimate")
    if not de:
        return None
    m = DROPS_NUM_RE.search(de)
    return float(m.group(1)) if m else None


def parse_issue_metadata(issue: dict) -> dict:
    body = issue.get("body") or ""
    chunk_id = _first_code(_section_body(body, "Chunk ID"))
    severity = _first_code(_section_body(body, "Severity"))
    queue = _first_code(_section_body(body, "Queue"))
    min_tier = _first_code(_section_body(body, "Min Contributor Tier"))
    claim_method = _first_code(_section_body(body, "Claim Method"))
    drops = _drops_estimate(body)
    return {
        "chunk_id": chunk_id,
        "severity": severity,
        "queue": queue,
        "min_tier": min_tier,
        "claim_method": claim_method,
        "drops": drops,
    }


# ---------- Per-consumer aggregation ----------

@dataclass
class ConsumerStats:
    name: str
    display_name: str
    repo: str
    contribute_url: str | None = None
    description: str = ""
    chunks_completed: int = 0
    chunks_active: int = 0
    chunks_claimable: int = 0  # active AND assignee=none
    tokens_estimated: int = 0
    tokens_actual: int = 0
    contributors_unique: int = 0
    sidecars_count: int = 0
    last_completed_at: str | None = None


def fetch_consumer_stats(consumer: dict) -> tuple[ConsumerStats, list[dict]]:
    """Returns (stats, claimable_chunks_list)."""
    stats = ConsumerStats(
        name=consumer["name"],
        display_name=consumer["display_name"],
        repo=consumer["repo"],
        contribute_url=consumer.get("contribute_url"),
        description=consumer.get("description", "").strip(),
    )

    # Chunk-task issues may be split across multiple repos. Historically OpenOnco
    # filed chunk issues in its own repo; from wave 5+ they live in
    # romeo111/task_torrent (the protocol repo). Allow consumers.yaml to declare
    # the full list of repos where chunk-task issues may be filed via
    # `chunk_issues_repos` (a list). Default falls back to the consumer's own
    # `repo` field for backwards compatibility.
    issues_repos = consumer.get("chunk_issues_repos") or [consumer["repo"]]
    issues: list = []
    for issues_repo in issues_repos:
        page = gh_paginated(f"repos/{issues_repo}/issues?labels=chunk-task&state=all&per_page=100")
        issues.extend(page)
    if not issues:
        return stats, []

    claimable: list[dict] = []
    for issue in issues:
        if "pull_request" in issue:
            continue  # skip PRs that GitHub returns as issues
        labels = {l.get("name", "") for l in (issue.get("labels") or [])}
        state = issue.get("state")
        is_completed = (
            state == "closed" and issue.get("state_reason") in (None, "completed")
        )
        is_active = state == "open" and "status-active" in labels

        if is_completed:
            stats.chunks_completed += 1
            ca = issue.get("closed_at") or issue.get("updated_at")
            if ca and (stats.last_completed_at is None or ca > stats.last_completed_at):
                stats.last_completed_at = ca

        if is_active:
            stats.chunks_active += 1
            assignees = issue.get("assignees") or []
            if not assignees:
                stats.chunks_claimable += 1
                meta = parse_issue_metadata(issue)
                claimable.append({
                    "consumer": consumer["name"],
                    "consumer_display": consumer["display_name"],
                    "issue_number": issue.get("number"),
                    "issue_url": issue.get("html_url"),
                    "title": (issue.get("title") or "").replace("[Chunk] ", "").strip(),
                    "chunk_id": meta["chunk_id"],
                    "severity": meta["severity"],
                    "queue": meta["queue"],
                    "min_tier": meta["min_tier"],
                    "claim_method": meta["claim_method"],
                    "drops": meta["drops"],
                    "created_at": issue.get("created_at"),
                })

    # Walk the consumer's contributions/ tree to read _contribution_meta.yaml
    # files and sum cost_actual.tokens (when present); count unique contributors.
    contrib_path = consumer.get("contributions_path", "contributions/").rstrip("/")
    tree_listing = gh_api(f"repos/{consumer['repo']}/git/trees/HEAD?recursive=1")
    if isinstance(tree_listing, dict):
        contributors: set[str] = set()
        for item in tree_listing.get("tree", []) or []:
            p = item.get("path", "")
            if not p.startswith(f"{contrib_path}/") or not p.endswith("/_contribution_meta.yaml"):
                continue
            stats.sidecars_count += 1
            meta_text = gh_raw_file(consumer["repo"], p)
            if not meta_text:
                continue
            try:
                meta = yaml.safe_load(meta_text)
            except yaml.YAMLError:
                continue
            if not isinstance(meta, dict):
                continue
            contrib_block = meta.get("_contribution") if "_contribution" in meta else meta
            if isinstance(contrib_block, dict):
                ca = contrib_block.get("cost_actual")
                if isinstance(ca, dict):
                    tokens = ca.get("tokens")
                    if isinstance(tokens, (int, float)):
                        stats.tokens_actual += int(tokens)
                contributor = contrib_block.get("contributor")
                if isinstance(contributor, str) and contributor:
                    contributors.add(contributor)
        stats.contributors_unique = len(contributors)

    return stats, claimable


def estimate_tokens_for_consumer(consumer: dict, stats: ConsumerStats) -> int:
    """Sum drops × TOKENS_PER_DROP across this consumer's chunk-spec files in
    the rules-repo (this repo's chunks/<consumer>/) plus claimable issues."""
    tokens = 0
    chunks_dir = REPO_ROOT / consumer.get("chunks_path", "").rstrip("/")
    if chunks_dir.is_dir():
        for spec in chunks_dir.glob("*.md"):
            if spec.name in ("README.md", "_example.md"):
                continue
            try:
                body = spec.read_text(encoding="utf-8")
            except OSError:
                continue
            d = _drops_estimate(body)
            if d is not None:
                tokens += int(d * TOKENS_PER_DROP)
    return tokens


# ---------- Build outputs ----------

def build() -> int:
    if not CONSUMERS_FILE.is_file():
        print(f"ERROR: {CONSUMERS_FILE} not found", file=sys.stderr)
        return 1
    cfg = yaml.safe_load(CONSUMERS_FILE.read_text(encoding="utf-8")) or {}
    consumers = cfg.get("consumers", [])
    if not consumers:
        print("WARN: no consumers registered; emitting empty data", file=sys.stderr)

    LANDING_DIR.mkdir(parents=True, exist_ok=True)

    per_consumer: list[dict] = []
    all_claimable: list[dict] = []
    totals = {
        "chunks_completed": 0,
        "chunks_active": 0,
        "chunks_claimable": 0,
        "tokens_estimated": 0,
        "tokens_actual": 0,
        "contributors_unique_global_estimate": 0,
        "sidecars_count": 0,
    }
    for consumer in consumers:
        try:
            stats, claimable = fetch_consumer_stats(consumer)
        except Exception as e:  # pragma: no cover (network)
            print(f"WARN: consumer {consumer.get('name')} fetch failed: {e}", file=sys.stderr)
            continue
        stats.tokens_estimated = estimate_tokens_for_consumer(consumer, stats)

        per_consumer.append({
            "name": stats.name,
            "display_name": stats.display_name,
            "repo": stats.repo,
            "contribute_url": stats.contribute_url,
            "description": stats.description,
            "chunks_completed": stats.chunks_completed,
            "chunks_active": stats.chunks_active,
            "chunks_claimable": stats.chunks_claimable,
            "tokens_estimated": stats.tokens_estimated,
            "tokens_actual": stats.tokens_actual,
            "contributors_unique": stats.contributors_unique,
            "sidecars_count": stats.sidecars_count,
            "last_completed_at": stats.last_completed_at,
        })

        for k in totals:
            if k == "contributors_unique_global_estimate":
                totals[k] += stats.contributors_unique
            elif k in {"chunks_completed", "chunks_active", "chunks_claimable",
                       "tokens_estimated", "tokens_actual", "sidecars_count"}:
                totals[k] += getattr(stats, k)

        all_claimable.extend(claimable)

    metrics = {
        "schema_version": "1",
        "last_updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": totals,
        "per_consumer": per_consumer,
    }

    chunks = {
        "schema_version": "1",
        "last_updated": metrics["last_updated"],
        "claimable": sorted(
            all_claimable,
            key=lambda c: (
                # Severity sort: high → medium → low → unknown
                {"high": 0, "medium": 1, "low": 2}.get((c.get("severity") or "").lower(), 3),
                c.get("consumer", ""),
                c.get("created_at", ""),
            ),
        ),
    }

    (LANDING_DIR / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (LANDING_DIR / "chunks.json").write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )

    print(f"Wrote {LANDING_DIR / 'metrics.json'}")
    print(f"  consumers={len(per_consumer)}  claimable_chunks={len(all_claimable)}")
    print(f"  totals: {json.dumps(totals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
