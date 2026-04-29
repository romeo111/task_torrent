# Chunk: bma-ua-signoff-workflow-schema-2026-04-29-0030

> Add `signed_off_by` + `signed_off_date` fields to BMA UA-translation review schema; backfill 0 for now.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`trusted`

## Queue

`C`

## Topic Labels

`schema-evolution`, `ua-translation`, `governance`

## Mission

BMA records have `ukrainian_review_status: pending_clinical_signoff` but no record of who signed off when status flips. Add `signed_off_by` (GitHub login or Co-Lead initials) and `signed_off_date` (ISO date). Backfill empty values on all 399 BMAs (no signoffs have happened yet).

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA UA-signed-off` instrumentation (currently 0%; Co-Lead signoff queue is the bottleneck).

## Economic Profile

```yaml
compute_profile: mechanical
verification_method: computational
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 1
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  Pure schema add + null backfill. Pydantic accepts. ~1 hour.
```

## Drop Estimate

~1 Drops (~100k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CHARTER §6.1 (two-reviewer signoff requirement).

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. Plus schema in `knowledge_base/schemas/biomarker_actionability.py`.

## Output Format

- `contributions/bma-ua-signoff-workflow-schema-2026-04-29-0030/bma_<id>.yaml` — upsert each (add fields, leave empty)
- `contributions/bma-ua-signoff-workflow-schema-2026-04-29-0030/schema_patch.diff` — Pydantic schema extension
- `contributions/bma-ua-signoff-workflow-schema-2026-04-29-0030/task_manifest.txt`
- `contributions/bma-ua-signoff-workflow-schema-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Every BMA has `signed_off_by: null` and `signed_off_date: null` after upsert.
- [ ] Pydantic schema extension validates existing 399 BMAs without error.
- [ ] No clinical content modified.

## Rejection Criteria

- Other fields modified.
- Schema field made required (must be Optional).

## Claim Method

`trusted-agent-wip-branch-first`
