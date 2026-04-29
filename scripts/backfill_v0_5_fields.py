"""One-off backfill: add Severity / Min Contributor Tier / Queue sections
to existing OpenOnco chunk specs and a kb-coverage-matrix reference to
Mission.

Run from task_torrent repo root:
    python scripts/backfill_v0_5_fields.py

The script is idempotent — running twice does not duplicate sections.
Skip a chunk by adding `# backfill-skip` as the first line of its file.

After running, re-run the linter:
    python -m tasktorrent.lint_chunk_spec --all chunks/openonco/

Per-chunk values are encoded inline below. Reasoning:
  - Severity: low (no clinical risk), medium (data with evidence),
    high (claim-bearing or bulk mutation)
  - Min Contributor Tier: new (safe to learn on), established
    (data ingestion), trusted (high blast radius)
  - Queue: A (coverage-fill), B (audit-remediate), C (schema-evolution)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple


class ChunkBackfill(NamedTuple):
    severity: str
    min_tier: str
    queue: str
    mission_addendum: str
    # Optional retroactive fills for legacy chunks
    economic_profile_yaml: str | None = None
    claim_method: str | None = None
    verifier_threshold: str | None = None
    set_status: str | None = None


_LEGACY_ECONOMIC_PROFILE = """```yaml
compute_profile: {compute}
verification_method: {verification}
break_even_test: {break_even}
output_type: {output_type}
backfilled_retroactively: true
backfilled_date: "2026-04-29"
```"""


def _econ(compute: str, verification: str, break_even: str, output_type: str) -> str:
    return _LEGACY_ECONOMIC_PROFILE.format(
        compute=compute, verification=verification,
        break_even=break_even, output_type=output_type,
    )


CHUNKS: dict[str, ChunkBackfill] = {
    "bma-drafting-gap-diseases.md": ChunkBackfill(
        severity="high", min_tier="trusted", queue="A",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Per-disease coverage matrix > "
            "Coverage gaps > Diseases with thin BMA` — fills BMA records for "
            "rare-disease subtypes currently at 0 or 1-2 entries."
        ),
        economic_profile_yaml=_econ("mixed", "full-expert", "PASS", "entity-sidecar"),
        claim_method="formal-issue",
    ),
    "citation-semantic-verify-v2.md": ChunkBackfill(
        severity="medium", min_tier="established", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA with CIViC evidence_sources` — improves citation grounding "
            "via semantic re-verification of v1 audit findings."
        ),
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
    ),
    "citation-verify-914-audit.md": ChunkBackfill(
        severity="medium", min_tier="established", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "Sources current_as_of <365d` — surfaces stale + broken citations "
            "across 464 entities."
        ),
        economic_profile_yaml=_econ("llm-essential", "sample", "PASS", "report-only"),
        claim_method="trusted-agent-wip-branch-first",
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
    ),
    "civic-bma-reconstruct-all.md": ChunkBackfill(
        severity="medium", min_tier="trusted", queue="C",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA with CIViC evidence_sources` — schema evolution from "
            "OncoKB-derived metadata to CIViC `evidence_sources` block."
        ),
        economic_profile_yaml=_econ("mechanical", "computational", "PASS", "entity-sidecar"),
        claim_method="trusted-agent-wip-branch-first",
    ),
    "drug-class-normalization.md": ChunkBackfill(
        severity="low", min_tier="new", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Top-level KPIs > Drugs` — "
            "normalizes drug_class string formatting (cleanup, no clinical risk). "
            "Retroactively withdrawn: 0 actionable normalizations found on 216 drugs (data already canonical). "
            "See L-20 / Proposal #20."
        ),
        set_status="withdrawn",
    ),
    "escat-tier-audit.md": ChunkBackfill(
        severity="high", min_tier="trusted", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > ESCAT tier distribution` — "
            "audits the 100% nominal ESCAT-tier coverage for actual semantic "
            "correctness (B2 subset projects ~10% overclaim risk)."
        ),
    ),
    "indication-line-of-therapy-audit.md": ChunkBackfill(
        severity="high", min_tier="trusted", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "Indications with NCCN category` — audits cited line-of-therapy "
            "evidence against the actual cited Source content."
        ),
    ),
    "rec-wording-audit-claim-bearing.md": ChunkBackfill(
        severity="high", min_tier="trusted", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA UA-signed-off` — fixes recommendation wording on "
            "claim-bearing fields where 229 critical issues need signoff."
        ),
        economic_profile_yaml=_econ("llm-essential", "full-expert", "PASS", "report-only"),
        claim_method="trusted-agent-wip-branch-first",
    ),
    "redflag-indication-coverage-fill.md": ChunkBackfill(
        severity="medium", min_tier="established", queue="A",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Per-disease coverage matrix > "
            "RF` — fills the 5-type RF matrix for diseases with partial coverage."
        ),
        economic_profile_yaml=_econ("mixed", "full-expert", "PASS", "entity-sidecar"),
        claim_method="formal-issue",
    ),
    "source-stub-ingest-batch.md": ChunkBackfill(
        severity="low", min_tier="new", queue="A",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Top-level KPIs > Sources` — "
            "ingests SRC-* stubs for cited but un-stubbed sources."
        ),
        economic_profile_yaml=_econ("mixed", "sample", "PASS", "entity-sidecar"),
        claim_method="formal-issue",
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
    ),
    "trial-source-ingest-pubmed.md": ChunkBackfill(
        severity="medium", min_tier="established", queue="A",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Top-level KPIs > Sources` — "
            "ingests pivotal-trial Source entities for un-stubbed RCT references."
        ),
        verifier_threshold=">=85% claims pass Anthropic Citations API grounding (default).",
    ),
    "ua-translation-review-batch.md": ChunkBackfill(
        severity="medium", min_tier="established", queue="B",
        mission_addendum=(
            "Advances `kb-coverage-matrix.md > Quality scores > "
            "BMA UA-signed-off` — reviews 1858 Ukrainian-translation findings "
            "across the KB."
        ),
        economic_profile_yaml=_econ("llm-essential", "sample", "PASS", "report-only"),
        claim_method="formal-issue",
    ),
}


def already_has_section(text: str, heading: str) -> bool:
    return re.search(rf"^##\s+{re.escape(heading)}\b", text, re.MULTILINE) is not None


def add_section_after_status(text: str, heading: str, value: str) -> str:
    """Insert `## <heading>\\n\\n<value>\\n` directly after the Status block."""
    if already_has_section(text, heading):
        return text
    # Find the Status block and the next ## heading after it
    status_match = re.search(r"^##\s+Status\b", text, re.MULTILINE)
    if not status_match:
        return text  # no Status — bail
    next_heading = re.search(r"^##\s+", text[status_match.end():], re.MULTILINE)
    if not next_heading:
        return text
    insertion_point = status_match.end() + next_heading.start()
    new_block = f"## {heading}\n\n`{value}`\n\n"
    return text[:insertion_point] + new_block + text[insertion_point:]


def add_matrix_ref_to_mission(text: str, addendum: str) -> str:
    """Append the matrix reference to the Mission body if not already present."""
    if "kb-coverage-matrix.md" in text:
        return text
    mission_match = re.search(r"^##\s+Mission\b", text, re.MULTILINE)
    if not mission_match:
        return text
    next_heading = re.search(r"^##\s+", text[mission_match.end():], re.MULTILINE)
    if not next_heading:
        return text
    body_end = mission_match.end() + next_heading.start()
    insertion = f"\n\n**KB coverage:** {addendum}\n"
    return text[:body_end] + insertion + text[body_end:]


def add_section_with_body(text: str, heading: str, body: str) -> str:
    """Insert a `## <heading>` section with a free-form body after Status."""
    if already_has_section(text, heading):
        return text
    status_match = re.search(r"^##\s+Status\b", text, re.MULTILINE)
    if not status_match:
        return text
    next_heading = re.search(r"^##\s+", text[status_match.end():], re.MULTILINE)
    if not next_heading:
        return text
    insertion_point = status_match.end() + next_heading.start()
    new_block = f"## {heading}\n\n{body}\n\n"
    return text[:insertion_point] + new_block + text[insertion_point:]


def update_status(text: str, new_status: str) -> str:
    """Replace the Status block's value (keeps heading, swaps content)."""
    pattern = re.compile(r"(^##\s+Status\s*\n\n)(.*?)(\n\n)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return text
    return text[:match.start()] + match.group(1) + f"`{new_status}`" + match.group(3) + text[match.end():]


def fix_invalid_verification_method(text: str) -> str:
    """drug-class-normalization had `full-maintainer-review` — coerce to `full-expert`."""
    return text.replace("full-maintainer-review", "full-expert")


def backfill_one(path: Path, cfg: ChunkBackfill) -> bool:
    """Apply backfill to a single chunk-spec file. Returns True if changed."""
    original = path.read_text(encoding="utf-8")
    if original.startswith("# backfill-skip"):
        return False

    text = original
    text = add_section_after_status(text, "Severity", cfg.severity)
    text = add_section_after_status(text, "Min Contributor Tier", cfg.min_tier)
    text = add_section_after_status(text, "Queue", cfg.queue)
    text = add_matrix_ref_to_mission(text, cfg.mission_addendum)
    if cfg.economic_profile_yaml and not already_has_section(text, "Economic Profile"):
        text = add_section_with_body(text, "Economic Profile", cfg.economic_profile_yaml)
    if cfg.claim_method and not already_has_section(text, "Claim Method"):
        text = add_section_with_body(text, "Claim Method", f"`{cfg.claim_method}`")
    if cfg.verifier_threshold and not already_has_section(text, "Verifier Threshold"):
        text = add_section_with_body(text, "Verifier Threshold", cfg.verifier_threshold)
    if cfg.set_status:
        text = update_status(text, cfg.set_status)
    text = fix_invalid_verification_method(text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    chunks_dir = repo_root / "chunks" / "openonco"
    if not chunks_dir.is_dir():
        print(f"ERROR: {chunks_dir} not found", file=sys.stderr)
        return 1

    changed = 0
    skipped = 0
    for filename, cfg in CHUNKS.items():
        path = chunks_dir / filename
        if not path.is_file():
            print(f"  SKIP {filename} (not found)")
            skipped += 1
            continue
        if backfill_one(path, cfg):
            print(f"  UPDATED {filename}")
            changed += 1
        else:
            print(f"  no-op  {filename}")

    print(f"\n{changed} chunks updated; {skipped} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
