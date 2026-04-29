# Chunk: rec-wording-critical-remediation-2026-04-29-0030

> Fix 229 critical rec-wording findings (claim-bearing fields with treatment-recommendation phrasing).

## Status

`queued`

## Severity

`high`

## Min Contributor Tier

`trusted`

## Queue

`B`

## Topic Labels

`audit`, `rec-wording`, `claim-bearing`, `safety`

## Mission

rec-wording-audit-claim-bearing (PR #17) flagged 229 critical findings where field text reads as treatment recommendation rather than evidence summary. CHARTER §8.3 forbids LLM-driven recommendations. Fix wording to evidence-statement form while preserving clinical substance.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA UA-signed-off` indirectly — fixed wording becomes signoff-eligible.

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 8
  expert_hours: 16
  expert_specialty: clinical-co-lead
break_even_rationale: >
  229 critical wording fixes. Each requires expert read because clinical
  substance must survive. ~5k tokens per fix.
```

## Drop Estimate

~3 Drops (~300k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

Original cited sources (re-read for evidence-statement form).

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

229 entity-field pairs from `cancer-autoresearch/contributions/rec-wording-audit-claim-bearing/audit-report.yaml` (severity: critical). Final manifest = 229 entity IDs in `task_manifest.txt`.

## Output Format

- `contributions/rec-wording-critical-remediation-2026-04-29-0030/<entity-id>.yaml` — upserts (field-level)
- `contributions/rec-wording-critical-remediation-2026-04-29-0030/task_manifest.txt`
- `contributions/rec-wording-critical-remediation-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Each upsert touches ONLY the flagged field (no scope creep).
- [ ] Reworded text passes the rec-wording linter (no recommendation phrasing).
- [ ] Clinical substance preserved (sample expert review).
- [ ] `ukrainian_review_status: pending_clinical_signoff` set after fix.

## Rejection Criteria

- Clinical content silently dropped during reword.
- Treatment recommendation in fix output.

## Claim Method

`trusted-agent-wip-branch-first`
