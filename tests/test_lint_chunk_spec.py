"""Tests for tasktorrent.lint_chunk_spec."""

from __future__ import annotations

from pathlib import Path

import pytest

from tasktorrent.lint_chunk_spec import (
    LintFinding,
    extract_yaml_block,
    has_placeholder,
    lint_chunk_spec,
    parse_sections,
    _extract_inline_value,
)


VALID_CHUNK_SPEC = """# Chunk: example

## Status

`queued`

## Topic Labels

`example`

## Mission

This chunk advances `kb-coverage-matrix.md > Per-disease coverage matrix > DIS-EXAMPLE > BMA` from 0 to ≥3 by adding actionability records for hot-spot variants. Mission is at least forty characters.

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`A`

## Economic Profile

```yaml
compute_profile: mixed
llm_essential_pct: 50
verification_method: sample
break_even_test: PASS
output_type: entity-sidecar
```

## Drop Estimate

~3 Drops (~300k tokens).

## Required Skill

`example-skill`

## Allowed Sources

PubMed, CIViC.

## Manifest

- BMA-EGFR-L858R-NSCLC
- BMA-BRAF-V600E-MELANOMA

## Output Format

- contributions/example/sidecar.yaml

## Acceptance Criteria

- All gates pass.

## Rejection Criteria

- Banned source used.

## Claim Method

`formal-issue`
"""


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_valid_spec_passes(tmp_path: Path) -> None:
    p = write(tmp_path, "valid.md", VALID_CHUNK_SPEC)
    result = lint_chunk_spec(p)
    assert result.passed
    assert not result.errors


def test_missing_required_section(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("## Mission\n\nThis chunk advances", "")
    p = write(tmp_path, "no_mission.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any("Mission" in f.section for f in result.errors if f.section)


def test_invalid_claim_method(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("`formal-issue`", "`open-bidding`")
    p = write(tmp_path, "bad_cm.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Claim Method" for f in result.errors)


def test_break_even_fail_rejected(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("break_even_test: PASS", "break_even_test: FAIL")
    p = write(tmp_path, "fail.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any("FAIL" in f.message for f in result.errors)


def test_marginal_without_expected_violations_warns(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("break_even_test: PASS", "break_even_test: MARGINAL")
    p = write(tmp_path, "marginal.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed  # warning, not error
    assert any("expected_violations" in f.message for f in result.warnings)


def test_marginal_with_expected_violations_clean(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "break_even_test: PASS",
        "break_even_test: MARGINAL\nexpected_violations: 50",
    )
    p = write(tmp_path, "marginal_ok.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed
    assert not result.warnings


def test_manifest_with_placeholder_rejected(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "- BMA-EGFR-L858R-NSCLC\n- BMA-BRAF-V600E-MELANOMA",
        "- <entity_id_1>\n- TODO list real entities",
    )
    p = write(tmp_path, "placeholder.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Manifest" and "placeholder" in f.message for f in result.errors)


def test_invalid_economic_profile_yaml(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "```yaml\ncompute_profile: mixed",
        "```yaml\ncompute_profile: : : invalid",
    )
    p = write(tmp_path, "bad_yaml.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed


def test_drop_estimate_no_number(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "~3 Drops (~300k tokens).",
        "Lots of work.",
    )
    p = write(tmp_path, "no_num.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Drop Estimate" for f in result.errors)


def test_invalid_compute_profile(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "compute_profile: mixed",
        "compute_profile: quantum",
    )
    p = write(tmp_path, "bad_cp.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any("compute_profile" in f.message for f in result.errors)


def test_short_mission_rejected(tmp_path: Path) -> None:
    long_mission = (
        "This chunk advances `kb-coverage-matrix.md > Per-disease coverage matrix > "
        "DIS-EXAMPLE > BMA` from 0 to ≥3 by adding actionability records for "
        "hot-spot variants. Mission is at least forty characters."
    )
    spec = VALID_CHUNK_SPEC.replace(long_mission, "Do stuff.")
    p = write(tmp_path, "short.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Mission" for f in result.errors)


def test_missing_yaml_block_in_econ_profile(tmp_path: Path) -> None:
    # Replace the YAML fence with prose
    spec = VALID_CHUNK_SPEC.replace(
        "```yaml\ncompute_profile: mixed",
        "compute_profile is mixed",
    ).replace("```\n\n## Drop Estimate", "\n\n## Drop Estimate")
    p = write(tmp_path, "no_yaml.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any("yaml" in f.message.lower() for f in result.errors)


# --- Unit-level helpers ---

def test_parse_sections_simple() -> None:
    md = "# Title\n\n## A\n\nA-body\n\n## B\n\nB-body\n"
    sections = parse_sections(md)
    assert sections == {"A": "A-body", "B": "B-body"}


def test_extract_yaml_block_handles_yml_fence() -> None:
    body = "Some prose.\n\n```yml\nfoo: 1\nbar: 2\n```\n\nMore prose."
    assert extract_yaml_block(body) == {"foo": 1, "bar": 2}


def test_extract_yaml_block_no_block_returns_none() -> None:
    assert extract_yaml_block("just prose") is None


def test_has_placeholder() -> None:
    assert has_placeholder("- <entity_id_1>")
    assert has_placeholder("TODO: fill in")
    assert not has_placeholder("- BMA-EGFR-L858R-NSCLC")


def test_extract_inline_value_backtick() -> None:
    assert _extract_inline_value("`formal-issue`") == "formal-issue"
    assert _extract_inline_value("Status is `queued` for now.") == "queued"


def test_extract_inline_value_bare() -> None:
    assert _extract_inline_value("queued") == "queued"


def test_extract_inline_value_multiword_returns_none() -> None:
    assert _extract_inline_value("This is a multi-word body with no clear value.") is None


# --- v0.5 soft-required fields (Severity / Min Contributor Tier / Queue) ---

def _strip_section(spec: str, heading: str) -> str:
    """Remove a `## <heading>` block and its body up to next `## ` heading."""
    import re as _re
    pattern = _re.compile(rf"^## {_re.escape(heading)}\b.*?(?=^## |\Z)", _re.MULTILINE | _re.DOTALL)
    return pattern.sub("", spec)


def test_missing_severity_warns_not_errors(tmp_path: Path) -> None:
    spec = _strip_section(VALID_CHUNK_SPEC, "Severity")
    p = write(tmp_path, "no_sev.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed  # warning only
    assert any(f.section == "Severity" for f in result.warnings)


def test_missing_min_tier_warns_not_errors(tmp_path: Path) -> None:
    spec = _strip_section(VALID_CHUNK_SPEC, "Min Contributor Tier")
    p = write(tmp_path, "no_tier.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed
    assert any(f.section == "Min Contributor Tier" for f in result.warnings)


def test_missing_queue_warns_not_errors(tmp_path: Path) -> None:
    spec = _strip_section(VALID_CHUNK_SPEC, "Queue")
    p = write(tmp_path, "no_q.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed
    assert any(f.section == "Queue" for f in result.warnings)


def test_invalid_severity_rejected(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("`medium`", "`extreme`")
    p = write(tmp_path, "bad_sev.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Severity" for f in result.errors)


def test_invalid_min_tier_rejected(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("`established`", "`elite`")
    p = write(tmp_path, "bad_tier.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Min Contributor Tier" for f in result.errors)


def test_invalid_queue_rejected(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("`A`", "`X`")
    p = write(tmp_path, "bad_q.md", spec)
    result = lint_chunk_spec(p)
    assert not result.passed
    assert any(f.section == "Queue" for f in result.errors)


# --- Mission references kb-coverage-matrix (Proposal #25) ---

def test_mission_without_matrix_ref_warns(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "This chunk advances `kb-coverage-matrix.md > Per-disease coverage matrix > "
        "DIS-EXAMPLE > BMA` from 0 to ≥3 by adding actionability records for "
        "hot-spot variants. Mission is at least forty characters.",
        "Just describes the chunk in some prose without referencing the matrix in any way at all.",
    )
    p = write(tmp_path, "no_mat_ref.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed  # warning only
    assert any(
        f.section == "Mission" and "kb-coverage-matrix" in f.message
        for f in result.warnings
    )


def test_mission_with_matrix_ref_clean(tmp_path: Path) -> None:
    p = write(tmp_path, "with_ref.md", VALID_CHUNK_SPEC)
    result = lint_chunk_spec(p)
    matrix_warnings = [
        f for f in result.warnings
        if f.section == "Mission" and "kb-coverage-matrix" in f.message
    ]
    assert matrix_warnings == []


# --- Verifier Threshold conditional (Proposal #23) ---

def test_citation_chunk_without_verifier_threshold_warns(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace("`example`", "`citation-verify`, `mechanical+judgment`")
    p = write(tmp_path, "cite.md", spec)
    result = lint_chunk_spec(p)
    assert result.passed  # warning only
    assert any(f.section == "Verifier Threshold" for f in result.warnings)


def test_non_citation_chunk_no_threshold_warning(tmp_path: Path) -> None:
    """A regular chunk without citation topic labels should NOT warn about threshold."""
    p = write(tmp_path, "regular.md", VALID_CHUNK_SPEC)
    result = lint_chunk_spec(p)
    threshold_warnings = [f for f in result.warnings if f.section == "Verifier Threshold"]
    assert threshold_warnings == []


def test_citation_chunk_with_verifier_threshold_clean(tmp_path: Path) -> None:
    spec = VALID_CHUNK_SPEC.replace(
        "`example`",
        "`citation-verify`",
    ).replace(
        "## Claim Method",
        "## Verifier Threshold\n\n≥85% claims pass Anthropic Citations API grounding.\n\n## Claim Method",
    )
    p = write(tmp_path, "cite_ok.md", spec)
    result = lint_chunk_spec(p)
    threshold_warnings = [f for f in result.warnings if f.section == "Verifier Threshold"]
    assert threshold_warnings == []


# --- Integration: run on real OpenOnco chunk specs ---

def test_lint_real_openonco_chunks_smoke() -> None:
    """Real chunks may have warnings but should not crash the linter."""
    chunks_dir = Path(__file__).parent.parent / "chunks" / "openonco"
    if not chunks_dir.is_dir():
        pytest.skip("openonco chunks not present")
    for md in chunks_dir.glob("*.md"):
        if md.name.lower() in ("readme.md", "_example.md"):
            continue
        result = lint_chunk_spec(md)
        # Smoke: linter doesn't blow up
        assert isinstance(result.findings, list)
