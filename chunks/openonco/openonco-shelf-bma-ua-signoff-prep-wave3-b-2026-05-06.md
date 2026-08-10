# Chunk: openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06

> BMA Ukrainian signoff prep wave 3B. Piece 27/30 of the 2026-05-06 OpenOnco TaskTorrent shelf expansion.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`A`

## Topic Labels

`ua-translate`, `clinical-review`, `bma-signoff`

## Mission

Execute one 10-Drop shelf piece for `BMA-UA-SIGNOFF-W3B`. The contributor produces reviewable sidecars or reports only under `contributions/openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06/`; hosted clinical content is not edited directly.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA UA-signed-off` by turning the listed work units into manifest-scoped draft outputs with source locators, uncertainty flags, and reviewer notes.

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: sample
break_even_test: PASS
output_type: review-sidecar
verification_cost:
  maintainer_hours: 2
  expert_hours: 2
  expert_specialty: ua-review
break_even_rationale: >
  This is sized as one full TaskTorrent piece: 10 Drops, roughly 1M tokens of
  source reading, draft synthesis, sidecar shaping, and reviewer-oriented
  rationale writing. Smaller fragments should stay off the public shelf.
```

## Drop Estimate

~10 Drops (~1.0M tokens).

## Required Skill

`ukrainian-clinical-review`

## Allowed Sources

Existing OpenOnco BMA sidecars, Ukrainian clinical terminology references, and source titles/locators already present in OpenOnco. Do not add new clinical claims.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

Exactly 10 drop-scoped work units. At issue-open time, maintainers may replace each `DROP-*` line with the final entity IDs, but the count and scope must stay within this chunk.

- `BMA-UA-SIGNOFF-W3B:DROP-01`
- `BMA-UA-SIGNOFF-W3B:DROP-02`
- `BMA-UA-SIGNOFF-W3B:DROP-03`
- `BMA-UA-SIGNOFF-W3B:DROP-04`
- `BMA-UA-SIGNOFF-W3B:DROP-05`
- `BMA-UA-SIGNOFF-W3B:DROP-06`
- `BMA-UA-SIGNOFF-W3B:DROP-07`
- `BMA-UA-SIGNOFF-W3B:DROP-08`
- `BMA-UA-SIGNOFF-W3B:DROP-09`
- `BMA-UA-SIGNOFF-W3B:DROP-10`

## Output Format

- `contributions/openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06/task_manifest.txt`
- `contributions/openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06/_contribution_meta.yaml`
- `contributions/openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06/drop_*.yaml` or topic-specific sidecars described in the opened issue body.

## Acceptance Criteria

- [ ] `task_manifest.txt` matches the opened issue manifest exactly.
- [ ] Every output row declares `ai_tool`, `ai_model`, `target_action`, and reviewer notes.
- [ ] Source-backed claims cite existing `SRC-*` IDs or include scoped `source_stub_*.yaml` files.
- [ ] Unclear evidence is marked `review_required` instead of being forced into a recommendation.
- [ ] No files outside `contributions/openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06/` are touched.

## Rejection Criteria

- Uses a banned source or invents unsupported `SRC-*` IDs.
- Produces patient-specific advice or hosted-content edits.
- Emits outputs outside the manifest scope.
- Omits uncertainty notes for weak, indirect, or inaccessible evidence.

## Claim Method

`formal-issue`
