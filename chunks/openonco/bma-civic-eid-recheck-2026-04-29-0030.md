# Chunk: bma-civic-eid-recheck-2026-04-29-0030

> Re-validate every CIViC EID in 399 BMA evidence_sources against current snapshot.

## Status

`queued`

## Severity

`low`

## Min Contributor Tier

`established`

## Queue

`B`

## Topic Labels

`audit`, `civic-evidence`, `computational`

## Mission

CIViC monthly snapshot refresh (commit `0b53a5c`) means EIDs from older snapshots may have been deprecated, merged, or had direction changed. This chunk re-validates every EID in every BMA's evidence_sources against the latest snapshot.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA with CIViC evidence_sources` quality dimension (verified-current EIDs).

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
  Pure mechanical: walk every BMA, look up each EID in snapshot. Re-verify
  by re-running the script.
```

## Drop Estimate

~2 Drops (~200k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC monthly snapshot under `knowledge_base/hosted/civic/`.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. Manifest = full file list.

## Output Format

- `contributions/bma-civic-eid-recheck-2026-04-29-0030/audit-report.yaml`
- `contributions/bma-civic-eid-recheck-2026-04-29-0030/task_manifest.txt`
- `contributions/bma-civic-eid-recheck-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Per-BMA row: total_eids, current_eids, deprecated_eids, direction_changed_eids.
- [ ] Output deterministic — re-running yields identical report.

## Rejection Criteria

- Non-deterministic output.
- Skipped BMAs without explanation.

## Claim Method

`trusted-agent-wip-branch-first`
