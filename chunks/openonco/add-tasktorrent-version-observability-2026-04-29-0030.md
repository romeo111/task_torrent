# Chunk: add-tasktorrent-version-observability-2026-04-29-0030

> Backfill `tasktorrent_version` (commit-hash style) into 12+ existing _contribution_meta.yaml files.

## Status

`queued`

## Severity

`low`

## Min Contributor Tier

`new`

## Queue

`C`

## Topic Labels

`schema-evolution`, `observability`

## Mission

L-21 / Proposal #27 introduces `_contribution.tasktorrent_version` as OPTIONAL observability field. This chunk backfills it on all existing `_contribution_meta.yaml` files in OpenOnco's `contributions/` tree, using each file's commit date as the version stamp.

**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs` instrumentation — post-hoc drift trace per L-21 across the contributions tree.

## Economic Profile

```yaml
compute_profile: mechanical
verification_method: computational
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 0.5
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  Pure mechanical backfill. <30 min total.
```

## Drop Estimate

~0.5 Drops (~50k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

git log of each contributions/<chunk-id>/ dir.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All `_contribution_meta.yaml` files under `cancer-autoresearch/contributions/`. Pre-activation: `find contributions -name '_contribution_meta.yaml'`. Currently ~12 chunk dirs.

## Output Format

- `contributions/add-tasktorrent-version-observability-2026-04-29-0030/<chunk-id>/_contribution_meta.yaml` — upsert each
- `contributions/add-tasktorrent-version-observability-2026-04-29-0030/task_manifest.txt`
- `contributions/add-tasktorrent-version-observability-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Every meta gets `tasktorrent_version: <YYYY-MM-DD-shortsha>` of its dir's first commit.
- [ ] No other field touched in any meta.

## Rejection Criteria

- Field added to non-meta files.
- Existing fields modified.

## Claim Method

`formal-issue`
