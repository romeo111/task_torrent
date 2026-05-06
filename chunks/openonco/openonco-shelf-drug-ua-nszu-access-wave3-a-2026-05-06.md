# Chunk: openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06

> Drug UA registration and NSZU access audit wave 3A. Piece 29/30 of the 2026-05-06 OpenOnco TaskTorrent shelf expansion.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`A`

## Topic Labels

`access-audit`, `drug-access`, `ua-context`

## Mission

Execute one 10-Drop shelf piece for `DRUG-UA-NSZU-W3A`. The contributor produces reviewable sidecars or reports only under `contributions/openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06/`; hosted clinical content is not edited directly.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > Drugs NSZU-reimbursed` by turning the listed work units into manifest-scoped draft outputs with source locators, uncertainty flags, and reviewer notes.

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: sample
break_even_test: PASS
output_type: report-sidecar
verification_cost:
  maintainer_hours: 2
  expert_hours: 2
  expert_specialty: access
break_even_rationale: >
  This is sized as one full TaskTorrent piece: 10 Drops, roughly 1M tokens of
  source reading, draft synthesis, sidecar shaping, and reviewer-oriented
  rationale writing. Smaller fragments should stay off the public shelf.
```

## Drop Estimate

~10 Drops (~1.0M tokens).

## Required Skill

`access-audit`

## Allowed Sources

Ukrainian public drug registry, NSZU public reimbursement/program pages, DailyMed/openFDA for identity cross-checks, and existing OpenOnco drug entities.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

Exactly 10 drop-scoped work units. At issue-open time, maintainers may replace each `DROP-*` line with the final entity IDs, but the count and scope must stay within this chunk.

- `DRUG-UA-NSZU-W3A:DROP-01`
- `DRUG-UA-NSZU-W3A:DROP-02`
- `DRUG-UA-NSZU-W3A:DROP-03`
- `DRUG-UA-NSZU-W3A:DROP-04`
- `DRUG-UA-NSZU-W3A:DROP-05`
- `DRUG-UA-NSZU-W3A:DROP-06`
- `DRUG-UA-NSZU-W3A:DROP-07`
- `DRUG-UA-NSZU-W3A:DROP-08`
- `DRUG-UA-NSZU-W3A:DROP-09`
- `DRUG-UA-NSZU-W3A:DROP-10`

## Output Format

- `contributions/openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06/task_manifest.txt`
- `contributions/openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06/_contribution_meta.yaml`
- `contributions/openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06/drop_*.yaml` or topic-specific sidecars described in the opened issue body.

## Acceptance Criteria

- [ ] `task_manifest.txt` matches the opened issue manifest exactly.
- [ ] Every output row declares `ai_tool`, `ai_model`, `target_action`, and reviewer notes.
- [ ] Source-backed claims cite existing `SRC-*` IDs or include scoped `source_stub_*.yaml` files.
- [ ] Unclear evidence is marked `review_required` instead of being forced into a recommendation.
- [ ] No files outside `contributions/openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06/` are touched.

## Rejection Criteria

- Uses a banned source or invents unsupported `SRC-*` IDs.
- Produces patient-specific advice or hosted-content edits.
- Emits outputs outside the manifest scope.
- Omits uncertainty notes for weak, indirect, or inaccessible evidence.

## Claim Method

`formal-issue`
