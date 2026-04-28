"""Chunk-spec linter — validates `chunks/<chunk-id>.md` against TaskTorrent v0.4 schema.

Required sections (all chunks):
  - Status            — must be `queued`, `status-active`, `completed`, `withdrawn`, etc.
  - Topic Labels
  - Mission           — non-empty prose
  - Economic Profile  — YAML block with break_even_test, compute_profile, verification_method
  - Drop Estimate     — non-empty
  - Required Skill
  - Allowed Sources
  - Manifest          — concrete entity IDs / files (not placeholder)
  - Output Format
  - Acceptance Criteria
  - Rejection Criteria
  - Claim Method      — must be `formal-issue` or `trusted-agent-wip-branch-first`

Conditional sections:
  - For MARGINAL chunks: `expected_violations` field in Economic Profile (Proposal #20).
  - For volume-mutating chunks: `volume_impact` declaration (Proposal #18).

Usage:
  python -m tasktorrent.lint_chunk_spec <path/to/chunk.md> [more.md ...]
  python -m tasktorrent.lint_chunk_spec --all chunks/

Exit codes:
  0 — all chunk specs pass
  1 — at least one chunk spec failed
  2 — usage / IO error
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REQUIRED_SECTIONS = (
    "Status",
    "Topic Labels",
    "Mission",
    "Economic Profile",
    "Drop Estimate",
    "Required Skill",
    "Allowed Sources",
    "Manifest",
    "Output Format",
    "Acceptance Criteria",
    "Rejection Criteria",
    "Claim Method",
)

VALID_STATUS = {
    "queued",
    "status-active",
    "active",
    "in-progress",
    "completed",
    "withdrawn",
    "blocked",
}

VALID_CLAIM_METHODS = {"formal-issue", "trusted-agent-wip-branch-first"}

VALID_BREAK_EVEN_TESTS = {"PASS", "MARGINAL", "FAIL"}

VALID_COMPUTE_PROFILES = {"mechanical", "llm-essential", "mixed"}

VALID_VERIFICATION_METHODS = {"computational", "sample", "full-expert", "none"}

PLACEHOLDER_MARKERS = (
    "<entity_id_",
    "<placeholder",
    "TODO",
    "TBD",
    "FIXME",
)


@dataclass
class LintFinding:
    severity: str  # "error" | "warning"
    section: str | None
    message: str

    def render(self, path: Path) -> str:
        loc = f"{path}::{self.section}" if self.section else str(path)
        return f"  [{self.severity.upper()}] {loc} — {self.message}"


@dataclass
class LintResult:
    path: Path
    findings: list[LintFinding] = field(default_factory=list)

    @property
    def errors(self) -> list[LintFinding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[LintFinding]:
        return [f for f in self.findings if f.severity == "warning"]

    @property
    def passed(self) -> bool:
        return not self.errors


SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_sections(markdown: str) -> dict[str, str]:
    """Split markdown into {section_heading: body} keyed by `## ` headings."""
    sections: dict[str, str] = {}
    matches = list(SECTION_RE.finditer(markdown))
    for i, m in enumerate(matches):
        heading = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        sections[heading] = body
    return sections


def extract_yaml_block(body: str) -> dict | None:
    """Extract the first ```yaml ... ``` fenced block from a section body."""
    fence_re = re.compile(r"```ya?ml\s*\n(.*?)\n```", re.DOTALL)
    m = fence_re.search(body)
    if not m:
        return None
    try:
        loaded = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None


def has_placeholder(text: str) -> bool:
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def lint_chunk_spec(path: Path) -> LintResult:
    """Lint a single chunk-spec markdown file. Returns LintResult."""
    result = LintResult(path=path)

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        result.findings.append(LintFinding("error", None, f"cannot read file: {e}"))
        return result

    sections = parse_sections(text)

    # 1. Required sections present
    for required in REQUIRED_SECTIONS:
        if required not in sections:
            result.findings.append(
                LintFinding("error", required, "required section missing")
            )

    # 2. Status valid
    if "Status" in sections:
        status_body = sections["Status"]
        status_value = _extract_inline_value(status_body)
        if status_value and status_value not in VALID_STATUS:
            result.findings.append(
                LintFinding(
                    "error",
                    "Status",
                    f"invalid value `{status_value}`; expected one of {sorted(VALID_STATUS)}",
                )
            )

    # 3. Claim Method valid
    if "Claim Method" in sections:
        cm_body = sections["Claim Method"]
        cm_value = _extract_inline_value(cm_body)
        if cm_value and cm_value not in VALID_CLAIM_METHODS:
            result.findings.append(
                LintFinding(
                    "error",
                    "Claim Method",
                    f"invalid value `{cm_value}`; expected one of {sorted(VALID_CLAIM_METHODS)}",
                )
            )

    # 4. Mission non-empty prose
    if "Mission" in sections and len(sections["Mission"].strip()) < 40:
        result.findings.append(
            LintFinding(
                "error",
                "Mission",
                "mission too short (<40 chars); chunk's purpose must be stated explicitly",
            )
        )

    # 5. Economic Profile parses + has required fields
    econ_break_even: str | None = None
    econ_compute_profile: str | None = None
    if "Economic Profile" in sections:
        econ = extract_yaml_block(sections["Economic Profile"])
        if econ is None:
            result.findings.append(
                LintFinding(
                    "error",
                    "Economic Profile",
                    "no parseable ```yaml ...``` block found",
                )
            )
        else:
            for required_field in ("compute_profile", "break_even_test", "verification_method"):
                if required_field not in econ:
                    result.findings.append(
                        LintFinding(
                            "error",
                            "Economic Profile",
                            f"missing required field `{required_field}`",
                        )
                    )

            cp = econ.get("compute_profile")
            if cp and cp not in VALID_COMPUTE_PROFILES:
                result.findings.append(
                    LintFinding(
                        "error",
                        "Economic Profile",
                        f"invalid compute_profile `{cp}`; expected one of {sorted(VALID_COMPUTE_PROFILES)}",
                    )
                )
            econ_compute_profile = cp

            be = econ.get("break_even_test")
            if be and be not in VALID_BREAK_EVEN_TESTS:
                result.findings.append(
                    LintFinding(
                        "error",
                        "Economic Profile",
                        f"invalid break_even_test `{be}`; expected one of {sorted(VALID_BREAK_EVEN_TESTS)}",
                    )
                )
            econ_break_even = be

            if be == "FAIL":
                result.findings.append(
                    LintFinding(
                        "error",
                        "Economic Profile",
                        "break_even_test=FAIL chunks must not be opened (per Proposal #1 decision rule)",
                    )
                )

            vm = econ.get("verification_method")
            if vm and vm not in VALID_VERIFICATION_METHODS:
                result.findings.append(
                    LintFinding(
                        "error",
                        "Economic Profile",
                        f"invalid verification_method `{vm}`; expected one of {sorted(VALID_VERIFICATION_METHODS)}",
                    )
                )

            # Conditional: MARGINAL chunks need expected_violations (Proposal #20)
            if be == "MARGINAL" and "expected_violations" not in econ:
                result.findings.append(
                    LintFinding(
                        "warning",
                        "Economic Profile",
                        "MARGINAL chunk should declare `expected_violations` (Proposal #20 / L-20) — without it, "
                        "maintainer cannot run pre-flight upstream-audit threshold check",
                    )
                )

    # 6. Manifest concrete (no placeholders)
    if "Manifest" in sections:
        manifest_body = sections["Manifest"]
        if not manifest_body.strip():
            result.findings.append(
                LintFinding("error", "Manifest", "manifest section empty")
            )
        elif has_placeholder(manifest_body):
            result.findings.append(
                LintFinding(
                    "error",
                    "Manifest",
                    "manifest contains placeholder text (TODO/TBD/<entity_id_…>); "
                    "must list real entity IDs or file paths",
                )
            )

    # 7. Drop Estimate non-empty + has a number
    if "Drop Estimate" in sections:
        de_body = sections["Drop Estimate"].strip()
        if not de_body:
            result.findings.append(
                LintFinding("error", "Drop Estimate", "drop estimate is empty")
            )
        elif not re.search(r"\d", de_body):
            result.findings.append(
                LintFinding(
                    "error",
                    "Drop Estimate",
                    "drop estimate has no numeric value (e.g., `~3 Drops`)",
                )
            )

    # 8. Allowed Sources non-empty
    if "Allowed Sources" in sections and len(sections["Allowed Sources"].strip()) < 5:
        result.findings.append(
            LintFinding(
                "warning",
                "Allowed Sources",
                "allowed-sources section is suspiciously short; declare allowed sources explicitly",
            )
        )

    return result


def _extract_inline_value(body: str) -> str | None:
    """Extract a single inline value from a section body.

    Handles forms like:
      - just a backtick value: `formal-issue`
      - prose with backtick: "claim method: `formal-issue`"
      - bare token: "queued"
    Returns None if no clear value can be extracted.
    """
    body = body.strip()
    if not body:
        return None
    # First backtick-quoted token wins
    bt = re.search(r"`([^`\n]+)`", body)
    if bt:
        return bt.group(1).strip()
    # If body is short enough and one token, return it
    first_line = body.split("\n", 1)[0].strip()
    if " " not in first_line and len(first_line) < 80:
        return first_line
    return None


def find_chunk_specs(roots: Iterable[Path]) -> list[Path]:
    """Discover chunk-spec files under given roots (recursive `.md` excluding READMEs/index)."""
    found: list[Path] = []
    for root in roots:
        if root.is_file():
            if root.suffix == ".md":
                found.append(root)
            continue
        if not root.is_dir():
            continue
        for md in sorted(root.rglob("*.md")):
            name = md.name.lower()
            if name in ("readme.md", "index.md", "_example.md"):
                continue
            found.append(md)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tasktorrent.lint_chunk_spec",
        description="Lint TaskTorrent chunk-spec markdown files against v0.4 schema.",
    )
    parser.add_argument("paths", nargs="+", help="chunk-spec files or directories")
    parser.add_argument(
        "--all",
        action="store_true",
        help="treat positional args as directories and recurse for *.md",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only print failing files",
    )
    args = parser.parse_args(argv)

    paths = [Path(p) for p in args.paths]
    if args.all:
        targets = find_chunk_specs(paths)
    else:
        targets = []
        for p in paths:
            if p.is_dir():
                targets.extend(find_chunk_specs([p]))
            else:
                targets.append(p)

    if not targets:
        print("No chunk-spec files found.", file=sys.stderr)
        return 2

    any_failed = False
    for path in targets:
        result = lint_chunk_spec(path)
        if not result.passed:
            any_failed = True
            print(f"FAIL {path}")
            for f in result.findings:
                print(f.render(path))
        elif result.warnings:
            if not args.quiet:
                print(f"PASS (with warnings) {path}")
                for f in result.warnings:
                    print(f.render(path))
        else:
            if not args.quiet:
                print(f"PASS {path}")

    if any_failed:
        print("\nLint failed — fix errors above before promoting chunk to status-active.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
