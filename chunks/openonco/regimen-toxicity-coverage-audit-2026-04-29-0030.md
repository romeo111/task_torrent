# Chunk: regimen-toxicity-coverage-audit-2026-04-29-0030

> Audit which of 244 regimens have CTCAE v5 toxicity grading; surface gaps.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`B`

## Topic Labels

`audit`, `regimen-data`, `toxicity`

## Mission

CTCAE v5 toxicity profiles are needed for safety-side rendering, but no current measurement of how many regimens have them. This chunk audits all 244 regimens for presence + completeness of `key_toxicities` block with CTCAE v5 grading.

**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > Regimens` quality (toxicity coverage; currently unmeasured per kb-coverage-strategy.md §"What we don't yet measure").

## Economic Profile

```yaml
compute_profile: mixed
verification_method: sample
break_even_test: PASS
output_type: report-only
verification_cost:
  maintainer_hours: 2
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  Audit-only chunk. ~244 regimens × ~5k tokens = 1.2M. Sample-verify 10%
  (24).
```

## Drop Estimate

~2 Drops (~200k tokens).

## Required Skill

`drug-evidence-mapping`

## Allowed Sources

FDA labels, CTCAE v5 reference, pivotal trial publications.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 244 regimens in `knowledge_base/hosted/content/regimens/`. Manifest = full file list.

## Output Format

- `contributions/regimen-toxicity-coverage-audit-2026-04-29-0030/audit-report.yaml`
- `contributions/regimen-toxicity-coverage-audit-2026-04-29-0030/task_manifest.txt`
- `contributions/regimen-toxicity-coverage-audit-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Per-regimen row: has_key_toxicities, has_ctcae_grades, missing_grades, completeness_score.
- [ ] Aggregate stats at top of report (% complete, % missing).

## Rejection Criteria

- Per-row verdict without inspecting actual yaml fields.

## Claim Method

`trusted-agent-wip-branch-first`
