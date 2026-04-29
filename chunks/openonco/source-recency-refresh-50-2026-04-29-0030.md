# Chunk: source-recency-refresh-50-2026-04-29-0030

> Refresh `current_as_of` and metadata for 50 stale Source entities (out of 240 stale-by-date).

## Status

`queued`

## Severity

`low`

## Min Contributor Tier

`established`

## Queue

`A`

## Topic Labels

`source-ingest`, `metadata-classification`, `recency`

## Mission

240 of 269 sources have `current_as_of < 365d ago`. This chunk samples 50 high-citation-count sources (NCCN, ESMO, FDA labels) and refreshes their `current_as_of` after re-checking their original URL, license, and version.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > Sources current_as_of <365d` from 10% upward.

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
  Mostly mechanical URL HEAD + version-string update. Computational re-
  verify = URL-resolves check.
```

## Drop Estimate

~1 Drops (~100k tokens).

## Required Skill

`citation-verification`

## Allowed Sources

Original source landing pages (NCCN, ESMO, FDA, journal sites).

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

50 SRC-* stable IDs selected by maintainer pre-activation, weighted toward:

- High citation count (referenced by many BMA/IND/RF)
- Guidelines (NCCN, ESMO) with annual revisions
- FDA labels (drugs with updated indications)

Final manifest committed as `task_manifest.txt`.

## Output Format

- `contributions/source-recency-refresh-50-2026-04-29-0030/src_<id>.yaml` — one per source (upsert)
- `contributions/source-recency-refresh-50-2026-04-29-0030/task_manifest.txt`
- `contributions/source-recency-refresh-50-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Each upsert preserves existing fields except `current_as_of`, `version`, `url` (if redirected).
- [ ] URL HEAD returns 200/301/302 (verified before commit).
- [ ] License classification unchanged (or change explicitly noted).

## Rejection Criteria

- License downgrade without justification.
- Adding new fields beyond recency.

## Verifier Threshold

>=85% claims pass Anthropic Citations API grounding (default).

## Claim Method

`trusted-agent-wip-branch-first`
