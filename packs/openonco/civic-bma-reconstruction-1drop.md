# OpenOnco Drop Pack: CIViC BMA Evidence Reconstruction (NSCLC subset)

## Pack ID

`openonco-civic-bma-reconstruction-1drop`

## Status

**Pilot Pack 1.** Recommended first pack because:

- The CIViC pivot (commit `c72e45b`, 2026-04-27) flagged 399 BMA files with `actionability_review_required: true`.
- Acceptance is deterministic: a CIViC EID resolves, the matcher hits, the source-native level maps to a known token.
- ESCAT tier is source-neutral and stable, so contributor outputs are easy to validate against existing ESCAT taxonomy.
- Output is sidecar-only — no risk of drifting `knowledge_base/hosted/content/` mid-review.

## Mission

For the NSCLC subset of `actionability_review_required: true` BMA files in OpenOnco, reconstruct each BMA's `evidence_sources` block from CIViC (CC0) using the fusion-aware matcher (`engine/civic_variant_matcher.py`, commit `1d16841`), drop legacy `SRC-ONCOKB` entries, and clear `actionability_review_required: false` only when the reconstruction is mechanically defensible.

This pack does not change `escat_tier` or `recommended_combinations` — those stay untouched and require Clinical Co-Lead review separately.

## Total

1 Drop (~100k tokens of structured AI work)

## Required Skills

- Biomarker extraction (primary)
- Citation verification (secondary — for the post-reconstruction citation pass)

## Allowed Sources

CIViC (CC0) only for `evidence_sources` reconstruction. Existing `primary_sources` entries (NCCN-by-reference, ESMO, etc.) stay verbatim. See `docs/openonco-pilot-workflow.md` §"Source allowlist" for the full table. **Do not introduce new `SRC-*` entries other than `SRC-CIVIC` and `SRC-CIVIC-EID-<n>` source stubs.**

## Output Format

Sidecar BMA YAMLs at `contributions/openonco-civic-bma-reconstruction-1drop/<chunk-id>/bma_<biomarker>_<variant>_nsclc.yaml`, plus `chunk_manifest.txt` and `_contribution_meta.yaml`. Each BMA file mirrors `BiomarkerActionability` schema with `_contribution:` wrapper. See `skills/biomarker-extraction.md` for the exact shape.

## Chunks

Partitioned by biomarker gene to ensure no two chunks touch the same BMA file. Each chunk's `chunk_manifest.txt` lists explicit `BMA-*` IDs.

| Chunk ID | Scope | Drop Estimate | Manifest (illustrative — final list set when chunk issue opens) |
| --- | --- | ---: | --- |
| `openonco-civic-bma-reconstruction-c1` | EGFR family | 0.25 | `BMA-EGFR-T790M-NSCLC`, `BMA-EGFR-EXON19DEL-NSCLC`, `BMA-EGFR-L858R-NSCLC`, `BMA-EGFR-EXON20INS-NSCLC`, `BMA-EGFR-C797S-NSCLC` |
| `openonco-civic-bma-reconstruction-c2` | ALK / ROS1 fusions | 0.20 | `BMA-ALK-EML4-V1-NSCLC`, `BMA-ALK-EML4-V3-NSCLC`, `BMA-ROS1-FUSION-NSCLC`, `BMA-ROS1-G2032R-NSCLC` |
| `openonco-civic-bma-reconstruction-c3` | KRAS / BRAF / MET | 0.20 | `BMA-KRAS-G12C-NSCLC`, `BMA-BRAF-V600E-NSCLC`, `BMA-MET-EXON14-NSCLC`, `BMA-MET-AMPLIFICATION-NSCLC` |
| `openonco-civic-bma-reconstruction-c4` | RET / NTRK / HER2 | 0.20 | `BMA-RET-FUSION-NSCLC`, `BMA-NTRK-FUSION-NSCLC`, `BMA-HER2-EXON20-NSCLC`, `BMA-HER2-AMPLIFICATION-NSCLC` |
| `openonco-civic-bma-reconstruction-c5` | Citation cleanup pass + wrap-up report | 0.15 | All BMA files modified by c1–c4 — re-verify each `evidence_sources[*]` against CIViC, emit `citation-report.yaml` |

## Per-chunk procedure

For each BMA in the manifest:

1. Read the existing BMA file from `knowledge_base/hosted/content/biomarker_actionability/`.
2. Identify the `(gene, variant_qualifier)` and the disease (`DIS-NSCLC`).
3. Use `engine/civic_variant_matcher.py` (or its CIViC API equivalent) to find matching CIViC Evidence Items for `(gene, variant, disease)`.
4. For each matched CIViC EID, build an `EvidenceSourceRef`:
   - `source: SRC-CIVIC`
   - `level:` source-native CIViC level token (`A` / `B` / `C` / `D` / `E`), verbatim.
   - `evidence_ids: ["EID<n>"]`
   - `direction:` CIViC direction (`supports` / `does_not_support` / null)
   - `significance:` CIViC significance label
   - `note:` short clinical note if the EID has one; otherwise null.
5. **Drop** any `evidence_sources` entry with `source: SRC-ONCOKB`.
6. Decide `actionability_review_required`:
   - `false` if the new CIViC-only `evidence_sources` non-empty AND ESCAT tier is unchanged AND none of the dropped OncoKB entries described a unique claim (e.g. resistance / off-label) not covered by CIViC.
   - `true` if reconstruction is incomplete or ESCAT tier may need re-evaluation. Explain in `_contribution.notes_for_reviewer`.
7. Leave `escat_tier`, `evidence_summary`, `regulatory_approval`, `recommended_combinations`, `contraindicated_monotherapy`, `primary_sources` untouched.
8. Update `last_verified` to today's date.
9. Write the sidecar with `_contribution.target_action: upsert` and `_contribution.target_entity_id: <BMA-id>`.

If any `(gene, variant)` does not resolve in CIViC: do NOT clear `actionability_review_required`. Submit the sidecar with `actionability_review_required: true` and `_contribution.notes_for_reviewer: "No CIViC EID found for <gene> <variant>; needs maintainer triage."`

## Acceptance Criteria

- Every BMA in the chunk manifest has exactly one sidecar file.
- Every sidecar passes `pytest tests/` and Pydantic validation (after `_contribution:` strip).
- Every `evidence_sources[*].source` is `SRC-CIVIC` or an existing legacy non-OncoKB source. No new `SRC-*` IDs introduced (except `SRC-CIVIC-EID-*` stubs if explicitly needed; CIViC itself is one entity).
- `escat_tier`, `recommended_combinations`, `contraindicated_monotherapy`, `primary_sources` unchanged from `main`.
- `last_verified` advanced to submission date.
- For each `actionability_review_required: false` flip, the contributor's notes explain *why* the reconstruction is mechanically defensible.

## Rejection Criteria

- Sidecar adds an OncoKB entry to `evidence_sources`.
- Sidecar invents a CIViC EID not actually returned by the matcher.
- Sidecar changes `escat_tier`, `evidence_summary`, or any field outside the procedure's allowlist.
- Sidecar references an entity outside the chunk manifest.
- Sidecar uses recommendation wording or patient-specific guidance anywhere.
- PR includes files outside `contributions/openonco-civic-bma-reconstruction-1drop/<chunk-id>/`.

## Reviewer

- Maintainer review (1) at PR merge.
- 2 of 3 Clinical Co-Leads at the maintainer-run upsert step (CHARTER §6.1) — happens after sidecars accumulate, not at each PR.

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Source links required for every evidence claim (`SRC-*` ID, not URL)
- No fake CIViC EIDs
- Maintainer + Clinical Co-Lead review required before sidecar payload reaches `knowledge_base/hosted/content/`
