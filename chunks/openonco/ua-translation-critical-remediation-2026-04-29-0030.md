# Chunk: ua-translation-critical-remediation-2026-04-29-0030

> Fix 200 critical UA-translation findings (mistranslations + missing UA copy on critical fields).

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`B`

## Topic Labels

`audit`, `ua-translation`, `remediation`

## Mission

ua-translation-review-batch (PR #21 family) produced 1858 findings; 200 are critical (mistranslation or missing UA copy on critical fields). Fix the 200 critical first.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA UA-signed-off` toward 100%.

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: sample
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 4
  expert_hours: 8
  expert_specialty: ukrainian-clinical-language
break_even_rationale: >
  200 critical UA fixes. ~3k tokens each. Sample-verify 30% by UA-fluent
  clinical reviewer.
```

## Drop Estimate

~2 Drops (~200k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

МОЗ України (clinical terminology), original sources.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

200 entity-field pairs from `cancer-autoresearch/contributions/ua-translation-review-batch/audit-report.yaml` (severity: critical). Final manifest = 200 entity IDs in `task_manifest.txt`.

## Output Format

- `contributions/ua-translation-critical-remediation-2026-04-29-0030/<entity-id>.yaml` — upserts
- `contributions/ua-translation-critical-remediation-2026-04-29-0030/task_manifest.txt`
- `contributions/ua-translation-critical-remediation-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] UA copy preserves clinical terminology consistent with МОЗ.
- [ ] No machine-translation artifacts (e.g. half-Ukrainian/half-English sentences).
- [ ] Each upsert touches ONLY the flagged field.

## Rejection Criteria

- Machine-translation literal output.
- Untranslated medical English left in UA field.

## Claim Method

`formal-issue`
