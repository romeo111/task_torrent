# OpenOnco Drop Pack: Pancreatic Biomarkers

## Pack ID

`openonco-pancreatic-biomarkers-1drop`

## Status

**Phase 2 candidate (after Pack 1 + Pack 2 close).** Pancreatic biomarker coverage is a documented gap in OpenOnco. This pack drafts BMA candidates only — `escat_tier` and `recommended_combinations` go to maintainers + Clinical Co-Leads for two-reviewer signoff before merging into hosted content.

## Mission

Draft BMA sidecar candidates for pancreatic adenocarcinoma (`DIS-PDAC`) biomarkers that have CIViC coverage. The pack does not write new `Indication` records. New `BIO-*` records may be drafted only when an existing `BIO-*` doesn't cover the variant.

## Total

1 Drop

## Required Skills

- Biomarker extraction
- Citation verification

## Allowed Sources

CIViC (CC0) primary. NCCN-by-reference (`SRC-NCCN-PANCREATIC-*`), ESMO open guideline references, FDA labels (DailyMed) for biomarker-context drug labels. See `docs/openonco-pilot-workflow.md` §"Source allowlist".

## Output Format

Sidecar BMA + Biomarker YAMLs at `contributions/openonco-pancreatic-biomarkers-1drop/<chunk-id>/`. Each chunk also emits a `citation-report.yaml` covering the rows it touched.

## Chunks

Partitioned by stable `BMA-*` ID prefix to guarantee no two chunks touch the same BMA file. (Topic-based partitioning — KRAS vs DNA-repair vs immunotherapy — was rejected because a KRAS-G12C BMA can be cited under both KRAS and immunotherapy contexts.)

| Chunk ID | Scope | Drop Estimate | Manifest (illustrative — final list set when chunk issue opens) |
| --- | --- | ---: | --- |
| `openonco-pancreatic-biomarkers-c1` | KRAS variants in PDAC | 0.20 | `BMA-KRAS-G12C-PDAC`, `BMA-KRAS-G12D-PDAC`, `BMA-KRAS-G12V-PDAC`, `BMA-KRAS-G12R-PDAC` |
| `openonco-pancreatic-biomarkers-c2` | BRCA / PALB2 / ATM (DDR) | 0.20 | `BMA-BRCA1-PATHOGENIC-PDAC`, `BMA-BRCA2-PATHOGENIC-PDAC`, `BMA-PALB2-PATHOGENIC-PDAC`, `BMA-ATM-PATHOGENIC-PDAC` |
| `openonco-pancreatic-biomarkers-c3` | MSI-H / dMMR / TMB | 0.20 | `BMA-MSI-HIGH-PDAC`, `BMA-DMMR-PDAC`, `BMA-TMB-HIGH-PDAC` |
| `openonco-pancreatic-biomarkers-c4` | Fusions (NTRK / NRG1 / ALK) | 0.20 | `BMA-NTRK-FUSION-PDAC`, `BMA-NRG1-FUSION-PDAC`, `BMA-ALK-FUSION-PDAC` |
| `openonco-pancreatic-biomarkers-c5` | Citation cleanup + duplicate flagging across c1–c4 | 0.20 | All BMA + BIO-* IDs touched by c1–c4 |

For each chunk, the chunk manifest names exactly which `BMA-*` IDs the contributor owns. Drafting a BMA outside the manifest is auto-rejected.

## Acceptance Criteria

- Every BMA in the chunk manifest has a sidecar (`target_action: new` if no existing `BMA-*`, `upsert` if it exists).
- Every claim in `evidence_summary`, `recommended_combinations`, `contraindicated_monotherapy`, `notes` is traceable to at least one entry in `primary_sources` or `evidence_sources`.
- `escat_tier` is from ESMO ESCAT criteria (Mateo et al. 2018). When the contributor cannot determine ESCAT mechanically, `actionability_review_required: true` and the reason in `_contribution.notes_for_reviewer`.
- New `BIO-*` records (when needed) follow `skills/biomarker-extraction.md` Biomarker schema.
- Duplicate candidates flagged with `target_action: flag_duplicate` and `duplicate_of: BMA-*`.
- Citation report covers every `(entity, claim, source)` triple introduced by the chunk.

## Rejection Criteria

- BMA proposes a `recommended_combinations` regimen the cited source does not name.
- New `Indication` (IND-*) drafted (out of scope for this pack — file in a future Indication-drafting pack).
- Recommendation wording or patient-specific guidance.
- BMA targeting `(biomarker, variant, disease)` outside the chunk manifest.
- New `Regimen` (REG-*) invented.
- PR touches files outside `contributions/openonco-pancreatic-biomarkers-1drop/<chunk-id>/`.

## Reviewer

- Maintainer review (1) at PR merge.
- 2 of 3 Clinical Co-Leads at maintainer-run upsert step (CHARTER §6.1).

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Source links required for every clinical claim (`SRC-*` ID, not URL)
- Unsupported claims must be flagged via `actionability_review_required: true`
- Maintainer + Clinical Co-Lead review required before sidecar payload reaches `knowledge_base/hosted/content/`
