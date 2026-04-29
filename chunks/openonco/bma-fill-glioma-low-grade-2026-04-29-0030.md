# Chunk: bma-fill-glioma-low-grade-2026-04-29-0030

> Add 5 BMA records for low-grade glioma (currently 0): IDH1, IDH2, MGMT, 1p19q, BRAF V600E.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`trusted`

## Queue

`A`

## Topic Labels

`bma-drafting`, `neuro-oncology`, `civic-evidence`

## Mission

Low-grade glioma (IDH-mutant, WHO grade 2) is currently at 0 BMA records despite its biomarker-driven archetype. Draft 5 BMAs covering the canonical molecular subtypes that drive treatment selection.

**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > Diseases with zero BMA` for `DIS-GLIOMA-LOW-GRADE`.

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 1
  expert_hours: 2
  expert_specialty: neuro-oncology
break_even_rationale: >
  5 well-characterized BMAs; vorasidenib is a 2024 first-in-class IDH
  inhibitor (INDIGO).
```

## Drop Estimate

~1 Drops (~100k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC, NCCN CNS 2025, ESMO Glioma 2023, INDIGO trial readout.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

5 BMAs:

- `BMA-IDH1-R132H-GLIOMA-LOW-GRADE` (vorasidenib — INDIGO trial)
- `BMA-IDH2-R172-GLIOMA-LOW-GRADE` (vorasidenib)
- `BMA-MGMT-METHYLATION-GLIOMA-LOW-GRADE` (TMZ benefit prediction)
- `BMA-1P19Q-CODELETION-GLIOMA-LOW-GRADE` (oligodendroglioma; PCV vs TMZ)
- `BMA-BRAF-V600E-GLIOMA-LOW-GRADE` (dabrafenib + trametinib)

## Output Format

- `contributions/bma-fill-glioma-low-grade-2026-04-29-0030/bma_*.yaml`
- `contributions/bma-fill-glioma-low-grade-2026-04-29-0030/task_manifest.txt`
- `contributions/bma-fill-glioma-low-grade-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] Every sidecar has ai_tool + ai_model.
- [ ] IDH1/IDH2 BMAs cite INDIGO trial (Mellinghoff 2023, NEJM).
- [ ] ESCAT tier IA for IDH (FDA-approved vorasidenib).
- [ ] No banned sources.

## Rejection Criteria

- Generic glioma evidence used.
- Vorasidenib indication off-label-extended.

## Claim Method

`formal-issue`
