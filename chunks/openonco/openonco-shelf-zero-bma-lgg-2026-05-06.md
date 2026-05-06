# Chunk: openonco-shelf-zero-bma-lgg-2026-05-06

> Low-grade glioma BMA expansion. Piece 05/30 of the 2026-05-06 OpenOnco TaskTorrent shelf expansion.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`trusted`

## Queue

`A`

## Topic Labels

`bma-drafting`, `coverage-gap`, `neuro-oncology`

## Mission

Execute one 10-Drop shelf piece for `DIS-GLIOMA-LOW-GRADE`. The contributor produces reviewable sidecars or reports only under `contributions/openonco-shelf-zero-bma-lgg-2026-05-06/`; hosted clinical content is not edited directly.

**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > Diseases with zero BMA` by turning the listed work units into manifest-scoped draft outputs with source locators, uncertainty flags, and reviewer notes.

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 2
  expert_hours: 2
  expert_specialty: neuro-oncology
break_even_rationale: >
  This is sized as one full TaskTorrent piece: 10 Drops, roughly 1M tokens of
  source reading, draft synthesis, sidecar shaping, and reviewer-oriented
  rationale writing. Smaller fragments should stay off the public shelf.
```

## Drop Estimate

~10 Drops (~1.0M tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC, PubMed abstracts, PubMed Central OA subset, ClinicalTrials.gov, NCCN/ESMO/ASCO guideline references, DailyMed/openFDA labels where drug claims are in scope.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

Exactly 10 drop-scoped work units. At issue-open time, maintainers may replace each `DROP-*` line with the final entity IDs, but the count and scope must stay within this chunk.

- `DIS-GLIOMA-LOW-GRADE:DROP-01`
- `DIS-GLIOMA-LOW-GRADE:DROP-02`
- `DIS-GLIOMA-LOW-GRADE:DROP-03`
- `DIS-GLIOMA-LOW-GRADE:DROP-04`
- `DIS-GLIOMA-LOW-GRADE:DROP-05`
- `DIS-GLIOMA-LOW-GRADE:DROP-06`
- `DIS-GLIOMA-LOW-GRADE:DROP-07`
- `DIS-GLIOMA-LOW-GRADE:DROP-08`
- `DIS-GLIOMA-LOW-GRADE:DROP-09`
- `DIS-GLIOMA-LOW-GRADE:DROP-10`

## Output Format

- `contributions/openonco-shelf-zero-bma-lgg-2026-05-06/task_manifest.txt`
- `contributions/openonco-shelf-zero-bma-lgg-2026-05-06/_contribution_meta.yaml`
- `contributions/openonco-shelf-zero-bma-lgg-2026-05-06/drop_*.yaml` or topic-specific sidecars described in the opened issue body.

## Acceptance Criteria

- [ ] `task_manifest.txt` matches the opened issue manifest exactly.
- [ ] Every output row declares `ai_tool`, `ai_model`, `target_action`, and reviewer notes.
- [ ] Source-backed claims cite existing `SRC-*` IDs or include scoped `source_stub_*.yaml` files.
- [ ] Unclear evidence is marked `review_required` instead of being forced into a recommendation.
- [ ] No files outside `contributions/openonco-shelf-zero-bma-lgg-2026-05-06/` are touched.

## Rejection Criteria

- Uses a banned source or invents unsupported `SRC-*` IDs.
- Produces patient-specific advice or hosted-content edits.
- Emits outputs outside the manifest scope.
- Omits uncertainty notes for weak, indirect, or inaccessible evidence.

## Claim Method

`formal-issue`
