# Chunk: civic-bma-reconstruct-all

## Status

`queued` (proposed first active chunk)

## Topic Labels

`civic-evidence`, `mechanical+judgment`, `pilot-active`

## Mission

For all 399 OpenOnco BMA files flagged `actionability_review_required: true`, reconstruct each BMA's `evidence_sources` block from the local CIViC snapshot, drop legacy `SRC-ONCOKB` entries, and clear `actionability_review_required: false` only when the reconstruction is mechanically defensible. Untouched: `escat_tier`, `evidence_summary`, `regulatory_approval`, `recommended_combinations`, `contraindicated_monotherapy`, `primary_sources`.

## Drop Estimate

~12 Drops (~1.2M tokens). 399 BMA × ~3k tokens average per BMA (read existing file, query CIViC, build EvidenceSourceRef entries, judgment, write sidecar, notes_for_reviewer).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC (CC0) only for `evidence_sources` reconstruction. No new `SRC-*` entries beyond `SRC-CIVIC`. The local snapshot at `cancer-autoresearch/knowledge_base/hosted/civic/<latest>/evidence.yaml` is the source of truth — do not query the live CIViC API for this chunk (snapshot version locks reproducibility).

## Manifest

All 399 BMA files matching `actionability_review_required: true` on `cancer-autoresearch` `feat/civic-primary` (or successor branch) at chunk-issue open time. Distribution by tumor:

| Tumor | Count | Tumor | Count |
|---|---:|---|---:|
| Ovarian | 39 | NOS | 13 |
| Breast | 36 | Melanoma | 11 |
| NSCLC | 35 | MCL | 11 |
| CRC | 27 | MDS-HR | 11 |
| AML | 22 | MM | 10 |
| Prostate | 20 | CLL | 10 |
| PDAC | 16 | GIST | 9 |
| Urothelial | 15 | GBM | 9 |
| Gastric | 15 | (others) | ~80 |
| Endometrial | 15 | | |

Maintainer commits the canonical `task_manifest.txt` (one BMA stable ID per line) into the chunk-task issue at open.

## Computation

For each BMA in the manifest, the contributor's AI tool performs:

1. **Read** existing BMA YAML from `cancer-autoresearch/knowledge_base/hosted/content/biomarker_actionability/`.
2. **Extract** `(gene, variant_qualifier, disease_id)`.
3. **Query** `engine.civic_variant_matcher.matches_civic_entry(...)` against the CIViC snapshot for matching evidence items.
4. **Build** `EvidenceSourceRef` entries — one per CIViC EID, fields copied verbatim:
   - `source: SRC-CIVIC`
   - `level:` source-native token (`A`/`B`/`C`/`D`/`E`)
   - `evidence_ids: ["EID<n>"]`
   - `direction: <Supports|Does Not Support|null>`
   - `significance: <CIViC label>`
5. **Drop** any existing `evidence_sources` entry with `source: SRC-ONCOKB`.
6. **Judgment: `actionability_review_required`.**
   - `false` if reconstruction is mechanically defensible: ≥ 1 CIViC EID found AND none of the dropped OncoKB claims describe something not covered by CIViC.
   - `true` otherwise; reason in `_contribution.notes_for_reviewer`.
7. **Update** `last_verified` to submission date.
8. **Write** sidecar at `contributions/civic-bma-reconstruct-all/bma_<biomarker>_<variant>_<disease>.yaml` with `_contribution.target_action: upsert`.

Untouched fields: `escat_tier`, `evidence_summary`, `regulatory_approval`, `recommended_combinations`, `contraindicated_monotherapy`, `primary_sources`, `notes`.

## Where computation happens

Contributor's machine, contributor's AI tool. Contributor needs:

- Read access to `cancer-autoresearch` repo (public).
- Read access to the local CIViC snapshot under `knowledge_base/hosted/civic/<date>/evidence.yaml`.
- Python 3.12 to call `civic_variant_matcher.py` (or the contributor's AI tool emulates the matcher's logic per `engine/civic_variant_matcher.py` source).

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation passes for all 399 sidecars (after `_contribution:` strip).
- `task_manifest.txt` ⊆ flagged BMA set on `main`.
- Every sidecar's `target_entity_id` exists in `cancer-autoresearch/main`.
- No `evidence_sources[*].source: SRC-ONCOKB` in any sidecar.
- All sidecars have `_contribution.ai_tool` and `_contribution.ai_model`.
- `git diff` lists only `contributions/civic-bma-reconstruct-all/...` files.

### Computational re-verify (100%)

The maintainer runs a script that, for each sidecar:

1. Re-queries `civic_variant_matcher` against the same snapshot for the same `(gene, variant, disease)`.
2. Confirms `set(sidecar.evidence_sources[*].evidence_ids)` ⊆ `set(matcher_results)` and `level`/`direction`/`significance` match the snapshot row for each EID.
3. Confirms no fields outside the procedure's allowlist (steps 1–8 above) changed vs `main`.

Any mismatch = batch-level rejection: contributor must re-run the offending BMAs and force-push.

### Sample human re-verify (5%)

Clinical Co-Lead reads ~20 randomly sampled sidecars and confirms:

- The `actionability_review_required: false` judgment is defensible (i.e. dropped OncoKB claims didn't carry information unique to OncoKB).
- The reconstruction does not subtly change clinical meaning (despite the rule that fields outside the allowlist stay untouched).

### Trust threshold

- Computational re-verify: 100% agreement required. Mismatches → reject batch.
- Sample human re-verify: ≥ 90% Co-Lead agreement on judgment defensibility. Below → reject batch and require re-execution by a different model/contributor.

## Output Format

One sidecar YAML per BMA. Schema in `skills/biomarker-extraction.md`. Plus `task_manifest.txt` (one BMA ID per line) and `_contribution_meta.yaml` (chunk-level provenance).

## Acceptance Criteria

- All pre-acceptance gates pass.
- Computational re-verify shows 100% agreement.
- Sample human re-verify ≥ 90%.
- Sidecars cleanly upsert to `knowledge_base/hosted/content/biomarker_actionability/` after `_contribution:` strip.

## Rejection Criteria

- Any computational re-verify mismatch.
- Any field outside the procedure's allowlist changed vs `main`.
- Sidecar references a non-existent `SRC-CIVIC-EID-*` (impossible if matcher was used; possible if the contributor invented EIDs).
- Recommendation wording in any field.

## Claim Method

`trusted-agent-wip-branch-first` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1, at PR merge.
- Clinical Co-Lead signoff: 2 of 3, at maintainer-run upsert step.
