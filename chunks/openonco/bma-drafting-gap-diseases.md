# Chunk: bma-drafting-gap-diseases

## Status

`queued`

## Topic Labels

`evidence-draft`, `claim-bearing`, `coverage-gap`

## Mission

For diseases with documented BMA coverage gaps (top candidates: PDAC, cholangiocarcinoma, GBM, sarcoma subtypes, rare leukemias), draft new `BiomarkerActionability` candidates from CIViC + ESMO/NCCN-by-reference + open guidelines. Output: per-BMA sidecars with `_contribution.target_action: new`, plus updated `Biomarker` (BIO-*) sidecars when a new biomarker variant is involved.

This is the "fill the holes" complement to `civic-bma-reconstruct-all` — that chunk fixes existing flagged BMAs; this chunk drafts BMAs for `(biomarker, variant, disease)` triples that have no entity yet.

## Drop Estimate

~15 Drops (~1.5M tokens). ~80 new BMA candidates × ~15k tokens per draft (search CIViC + read multiple guideline sections + synthesize evidence_summary + map ESCAT + draft regulatory_approval + write notes_for_reviewer + handle BIO-* if needed).

## Required Skill

`biomarker-extraction` (drafting mode, not reconstruction).

## Allowed Sources

Full pilot allowlist. Expected primary sources: CIViC, NCCN-by-reference, ESMO/ASCO open guidelines, FDA labels via DailyMed, PubMed abstracts for emerging evidence.

## Manifest

The maintainer commits the canonical list of `(BIO-*, variant_qualifier, DIS-*)` triples to draft, derived from:

- `cancer-autoresearch/docs/reviews/bma-coverage-2026-04-27.md` (23 known BMA drafts pending)
- Per-disease gap analysis: PDAC (KRAS variants beyond G12C, BRCA partner genes), cholangio (FGFR2 fusions, IDH1/2), GBM (MGMT promoter, EGFR vIII), GIST (KIT exon ranges, PDGFRA), rare leukemias (uncommon fusions)

Expected manifest size: ~60–100 BMA triples, plus ~10–20 new BIO-* candidates if variant taxonomy gaps surface.

## Computation

For each `(biomarker, variant, disease)` triple:

1. **Check existence** — confirm no existing BMA-* on `main` covers this triple. Confirm `BIO-*` for the biomarker exists; if not, note for BIO-* drafting.
2. **Search CIViC** — use `engine/civic_variant_matcher.py` against the snapshot for `(gene, variant, disease)` evidence items.
3. **Search guidelines** — NCCN section reference, ESMO MCBS table, ASCO recommendations specific to the triple.
4. **Search FDA** — DailyMed / openFDA for drug labels naming the biomarker as a CDx or trial-restriction criterion.
5. **Synthesize `evidence_summary`** — 1–3 sentences neutral, source-attested.
6. **Build `evidence_sources`** — CIViC EIDs + NCCN section reference + FDA label reference, each as `EvidenceSourceRef`.
7. **Map ESCAT tier** from evidence portfolio (Mateo et al. 2018 Ann Oncol 29:1895). When evidence is borderline, set tier to closest-but-conservative (e.g. IIA over IB if data is single-arm) and explain in `notes_for_reviewer`.
8. **Build `regulatory_approval`** — verbatim FDA/EMA approval strings from labels.
9. **Build `recommended_combinations`** — only regimens explicitly named in cited sources for this exact triple.
10. **Set `actionability_review_required: true`** — every new BMA from this chunk requires Clinical Co-Lead signoff regardless. Contributors do not clear this flag.
11. **Write sidecar** at `contributions/bma-drafting-gap-diseases/bma_<biomarker>_<variant>_<disease>.yaml`.
12. **For new BIO-*** — write `bio_<biomarker>.yaml` with `actionability_lookup` populated.

## Where computation happens

Contributor's machine. Required:

- Read access to `cancer-autoresearch` (existing BMA / BIO / Source / Disease entities).
- Read access to local CIViC snapshot.
- Web access for ESMO / ASCO / DailyMed / openFDA.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on every sidecar.
- Every `target_entity_id` is genuinely new (no collision with `main`).
- Every `(biomarker_id, variant_qualifier, disease_id)` triple is unique within the chunk and not present on `main`.
- Every `evidence_sources[*].source` exists on `main` OR has a `source_stub.yaml` in the chunk dir.
- `actionability_review_required: true` on all new BMA (contributors must not flip it to false).
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify (CIViC subset)

Maintainer runs `civic_variant_matcher` on each BMA's `(gene, variant, disease)`. Confirms claimed CIViC EIDs ⊆ matcher results. EID inventions → reject sidecar.

### Sample human re-verify (100%)

This chunk produces claim-bearing new entities. **Every BMA gets a Clinical Co-Lead read.** No sample-only acceptance.

### Trust threshold

- Pre-acceptance gates: 100%.
- Computational CIViC re-verify: 100%.
- 2 of 3 Clinical Co-Leads sign off on each BMA at upsert step.

## Output Format

Per-triple sidecar:

- `bma_<biomarker>_<variant>_<disease>.yaml` — BMA candidate
- `bio_<biomarker>.yaml` — Biomarker candidate (only when new)
- `source_stub_<src_id>.yaml` — Source stub (only when new SRC-* needed)

Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- All gates pass.
- All CIViC EIDs verified.
- All BMAs reviewed by Co-Leads; 2/3 signoff per BMA.

## Rejection Criteria

- BMA names `recommended_combinations` not attested by cited sources.
- New BMA collides with existing entity ID.
- ESCAT tier overclaim (e.g. IA on single-arm trial evidence).
- `actionability_review_required: false` on contributor-authored sidecar.
- Recommendation wording.
- Invented CIViC EIDs.

## Reviewer

- Maintainer: 1.
- Clinical Co-Lead signoff: 2 of 3 per BMA at upsert.

## Notes

Highest clinical-evidence-creation risk in the shelf. Tractable by AI tool but requires patient, careful drafting. Do not open before `civic-bma-reconstruct-all` validates the workflow and reviewer cadence.
