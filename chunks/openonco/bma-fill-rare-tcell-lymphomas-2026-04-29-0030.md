# Chunk: bma-fill-rare-tcell-lymphomas-2026-04-29-0030

> Add >=3 BMA records each for 7 rare T-cell lymphomas currently at 0-2 BMA coverage.

## Status

`queued`

## Severity

`high`

## Min Contributor Tier

`trusted`

## Queue

`A`

## Topic Labels

`bma-drafting`, `rare-disease`, `lymphoma`, `civic-evidence`

## Mission

Draft new biomarker_actionability records for 7 rare T-cell lymphomas currently at 0-2 BMA coverage in the OpenOnco KB. Each disease gets >=3 actionable biomarkers with CIViC-backed `evidence_sources` blocks where available, otherwise NCCN/ESMO citations.

**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > Diseases with zero BMA` from 14 to 7 (and `Diseases with thin BMA` from 25 to ~22) by filling rare T-cell lymphoma rows.

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 6
  expert_hours: 8
  expert_specialty: hematopathology
break_even_rationale: >
  Manual rare-disease BMA drafting takes ~30 min per record × 21 = 10.5h.
  Contributor at ~12k tokens/BMA = 250k tokens. Sample-verify 30% (~6
  BMAs) = 6h maintainer + 8h expert. Net win ~5h after expert review.
```

## Drop Estimate

~3 Drops (~300k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC, NCCN T-cell Lymphoma 2025, ESMO PTCL 2024, PubMed RCTs.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA` (always banned per CHARTER §2).

## Manifest

Diseases (7), each gets >=3 BMA records. Suggested biomarkers per disease:

- `DIS-ATLL` — HTLV-1 status, IRF4 (mogamulizumab), CD25 (denileukin diftitox), CCR4
- `DIS-EATL` — celiac association, JAK1/STAT3 mutations, type II EBV-negative subtype
- `DIS-HSTCL` — STAT3/STAT5B mutations, isochromosome 7q, SETD2 mutations
- `DIS-MF-SEZARY` — CD30 expression (brentuximab vedotin), KIR3DL2 (mogamulizumab), TOX
- `DIS-NK-T-NASAL` — EBV titer, PD-L1 expression, DDX3X mutations
- `DIS-PTCL-NOS` — CD30, GATA3 vs TBX21 subtype, ALK status (rule out ALCL)
- `DIS-T-PLL` — TCL1A overexpression, ATM mutation/del, JAK3 mutations

Final manifest will list >=21 BMA stable IDs of form `BMA-<GENE>-<VARIANT>-<DISEASE>`.

## Output Format

- `contributions/bma-fill-rare-tcell-lymphomas-2026-04-29-0030/bma_<...>.yaml` — one per BMA
- `contributions/bma-fill-rare-tcell-lymphomas-2026-04-29-0030/task_manifest.txt`
- `contributions/bma-fill-rare-tcell-lymphomas-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] Every sidecar has `_contribution.ai_tool` and `_contribution.ai_model` set.
- [ ] PR branch matches `tasktorrent/bma-fill-rare-tcell-lymphomas-2026-04-29-0030`.
- [ ] task_manifest.txt lists >=21 BMA stable IDs.
- [ ] Every BMA has `disease_id`, `biomarker_id`, `escat_tier`, `evidence_sources`.
- [ ] `ukrainian_review_status: pending_clinical_signoff` on every record.
- [ ] No banned source references.

## Rejection Criteria

- Citation grounding fails verifier (any layer).
- Disease IDs outside the 7 listed.
- ESCAT tier inflated above evidence supports.
- Patient-specific output.

## Claim Method

`formal-issue`
