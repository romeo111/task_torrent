# Chunk: redflag-indication-coverage-fill

## Status

`queued`

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
backfilled_retroactively: true
backfilled_date: "2026-04-29"
```

## Queue

`A`

## Min Contributor Tier

`established`

## Severity

`medium`

## Topic Labels

`evidence-draft`, `coverage-gap`, `claim-bearing`

## Mission

For each `(disease, redflag)` cell empty in the 65-disease coverage matrix (`cancer-autoresearch/docs/reviews/redflag-indication-coverage-2026-04-27.md`), draft a sourced answer to "does this redflag apply to this disease, and if so, what's the alternative-track Indication trigger?". Output: per-cell sidecar with `_contribution.target_action: new` for the proposed RedFlag-Indication linkage, plus citation evidence.

The 65-disease coverage matrix is the canonical "what's missing" report from prior audit. Many cells are intentionally empty (redflag doesn't apply); the chunk drafts the explicit `not_applicable` declaration with rationale, OR drafts the linkage when applicable.



**KB coverage:** Advances `kb-coverage-matrix.md > Per-disease coverage matrix > RF` — fills the 5-type RF matrix for diseases with partial coverage.
## Drop Estimate

~15 Drops (~1.5M tokens). 65 diseases × ~30 redflags × ~800 tokens average per cell judgment + sidecar.

## Required Skill

Hybrid: `biomarker-extraction` (for evidence handling) + clinical-judgment (for applicability decisions). Strict source-citation discipline required — see allowed sources.

## Allowed Sources

Per `docs/openonco-pilot-workflow.md` §"Source allowlist". Heavy reliance expected on:

- ESMO / ASCO open guidelines
- NCCN by reference (section locator)
- DailyMed / openFDA for drug-side red flags
- PubMed abstracts (case-series for rare disease + RF combinations)

## Manifest

Empty cells from the 65×~30 matrix — exact count published when the chunk-task issue opens (matrix has a deterministic empty-cell set). Maintainer commits `task_manifest.txt` listing `(DIS-*, RF-*)` pairs.

Cells split into three target_action categories:

- `applicable` — RF triggers an alternative-track Indication for this disease → draft IND-* linkage.
- `not_applicable` — RF doesn't apply (e.g. liver-specific RF for non-hepatic cancer) → draft `not_applicable: true` declaration with sourced rationale.
- `uncertain` — needs Clinical Co-Lead. Mark explicitly; do not guess.

## Computation

For each `(disease, redflag)` cell:

1. **Read** the disease entity (`DIS-*`) and the redflag entity (`RF-*`) on `cancer-autoresearch/main`.
2. **Search** allowed sources for guidance specific to this combination — drug interaction → disease, organ-impairment → therapy class, age/comorbidity-specific contraindication, etc.
3. **Decide** target_action: `applicable` / `not_applicable` / `uncertain`.
4. **For `applicable`**:
   - Draft an `Indication` sidecar (or, when the linkage is already an existing IND-*, an annotation pointing at it). Set `red_flags_triggering_alternative: [RF-*]`.
   - Cite ≥ 1 source attesting the redflag-driven alternative.
5. **For `not_applicable`**:
   - Write a 1-sentence rationale + ≥ 1 source attesting the non-applicability (or, when the case is structurally obvious like "hepatotoxicity RF for radiation-only treated localized disease", explain the structural reasoning and don't force a source).
6. **For `uncertain`**:
   - Mark explicitly. Provide whatever partial evidence found. Do not draft an Indication.
7. **Write sidecar(s)** under `contributions/redflag-indication-coverage-fill/`.

## Where computation happens

Contributor's machine. Required:

- Read access to `cancer-autoresearch`.
- Web access for guideline / PubMed search.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on every sidecar.
- Manifest scope (every cell sidecared = every cell in `task_manifest.txt`; no extras).
- All `applicable` sidecars cite ≥ 1 existing `SRC-*` (or accompany a `source_stub.yaml`).
- All `not_applicable` declarations cite a source OR include structural reasoning ≥ 200 chars.
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify

None. This chunk is genuinely judgment-driven; no mechanical re-execution applies.

### Sample human re-verify (100% for `applicable`, 25% for `not_applicable`)

- **`applicable` cells: 100% Co-Lead read.** This is claim-bearing clinical content; nothing is accepted on sample.
- **`not_applicable` cells: 25% Co-Lead read.** Spot-check that the structural reasoning is sound or the source is correctly cited.
- **`uncertain` cells: 100% Co-Lead read.** These are deferred to Co-Lead anyway.

### Trust threshold

- For `applicable`: 2 of 3 Clinical Co-Leads must sign off per CHARTER §6.1 at upsert step. PR can merge to `main` (sidecars only) after 1 maintainer review; clinical signoff is the upsert gate.
- For `not_applicable`: ≥ 90% Co-Lead agreement on sample. Below → reject batch.

## Output Format

Per-cell sidecar files in `contributions/redflag-indication-coverage-fill/`:

```
ind_<disease>_<line>_<redflag-track>.yaml      # for applicable cells
rfx_<disease>_<redflag>_not_applicable.yaml    # for not_applicable cells
rfx_<disease>_<redflag>_uncertain.yaml         # for uncertain cells
```

Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- All gates pass.
- 100% Co-Lead read of `applicable` cells, 2/3 signoff.
- ≥ 90% Co-Lead agreement on sample of `not_applicable`.

## Rejection Criteria

- `applicable` cell with no source citation.
- `not_applicable` declaration that contradicts cited source.
- `applicable` Indication invents a `recommended_regimen` not attested by source.
- Recommendation wording in `rationale` or `notes`.

## Claim Method

`trusted-agent-wip-branch-first` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1.
- Clinical Co-Lead signoff: 2 of 3 for `applicable`; 1 of 3 sample-check for `not_applicable` and `uncertain`.

## Notes

This is the highest clinical-risk chunk in the shelf. Open it only after `civic-bma-reconstruct-all` and `citation-verify-914-audit` have validated the workflow. Consider running with a smaller sub-manifest (e.g. 10 diseases × 30 RFs = 300 cells) for the first iteration.
