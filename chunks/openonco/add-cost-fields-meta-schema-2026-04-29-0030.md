# Chunk: add-cost-fields-meta-schema-2026-04-29-0030

> Add optional `cost_estimate` (chunk-spec) + `cost_actual` (_contribution_meta.yaml) fields per protocol-v0.4.

## Status

`queued`

## Severity

`low`

## Min Contributor Tier

`trusted`

## Queue

`C`

## Topic Labels

`schema-evolution`, `observability`, `tooling`

## Mission

protocol-v0.4-design.md `Owner-resolved decisions` §2 commits to optional cost_estimate (chunk-spec) and cost_actual (`_contribution_meta.yaml`) fields. Add Pydantic schema + validator support + lint_chunk_spec soft-warning when missing on chunks ≥2 Drops.

**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs` instrumentation (tracks token economy of contributor work).

## Economic Profile

```yaml
compute_profile: mechanical
verification_method: computational
break_even_test: PASS
output_type: report-only
verification_cost:
  maintainer_hours: 1
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  Pure schema add. Tests cover the new fields. Fast.
```

## Drop Estimate

~1 Drops (~100k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

protocol-v0.4-design.md owner-resolved decisions section.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

Schema files to extend:

- `task_torrent/tasktorrent/lint_chunk_spec.py` — accept `cost_estimate` block
- `cancer-autoresearch/scripts/tasktorrent/validate_contributions.py` — accept `cost_actual` in meta
- `cancer-autoresearch/scripts/tasktorrent/_contribution_meta.example.yaml` (if exists) — example

No KB content changes. Test additions only.

## Output Format

- `contributions/add-cost-fields-meta-schema-2026-04-29-0030/<patch>.diff` — git format-patches against both repos
- `contributions/add-cost-fields-meta-schema-2026-04-29-0030/task_manifest.txt`
- `contributions/add-cost-fields-meta-schema-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Both validators accept new fields without warning.
- [ ] lint_chunk_spec emits warning (not error) on chunks >=2 Drops without cost_estimate.
- [ ] Tests for new schema branches pass.

## Rejection Criteria

- Field made required (must stay optional per owner decision).
- Tests skipped.

## Claim Method

`trusted-agent-wip-branch-first`
