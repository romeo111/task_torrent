# Chunk: bma-fill-soft-tissue-rare-2026-04-29-0030

> Add BMA records for IMT, MPNST, Chondrosarcoma (currently 0 each).

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`trusted`

## Queue

`A`

## Topic Labels

`bma-drafting`, `sarcoma`, `rare-disease`, `civic-evidence`

## Mission

Three rare soft-tissue/bone sarcomas are at 0 BMA: inflammatory myofibroblastic tumor (ALK fusion-driven), MPNST (NF1 / EED-SUZ12 / CDKN2A loss), and chondrosarcoma (IDH1/2). Draft >=2 BMAs per disease.

**KB coverage:** Advances `kb-coverage-matrix.md > Coverage gaps > Diseases with zero BMA` for 3 sarcomas.

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 2
  expert_hours: 3
  expert_specialty: sarcoma
break_even_rationale: >
  6 BMAs across 3 rare diseases. Sarcoma expert needed for tier accuracy.
```

## Drop Estimate

~1.5 Drops (~150k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

CIViC, NCCN Sarcoma 2025, ESMO Sarcoma 2021, PubMed.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

6 BMAs (2 per disease minimum):

- `BMA-ALK-FUSION-IMT` (crizotinib / lorlatinib)
- `BMA-ROS1-FUSION-IMT` (entrectinib; rare subset)
- `BMA-NF1-LOSS-MPNST` (no targeted therapy; chemo + RT)
- `BMA-SUZ12-EED-LOSS-MPNST` (PRC2 loss; experimental)
- `BMA-IDH1-CHONDROSARCOMA` (ivosidenib clinical trial evidence)
- `BMA-IDH2-CHONDROSARCOMA` (enasidenib clinical trial evidence)

## Output Format

- `contributions/bma-fill-soft-tissue-rare-2026-04-29-0030/bma_*.yaml`
- `contributions/bma-fill-soft-tissue-rare-2026-04-29-0030/task_manifest.txt`
- `contributions/bma-fill-soft-tissue-rare-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] ALK fusion BMA correctly distinguishes IMT from anaplastic-LCL evidence.
- [ ] MPNST BMAs honestly report no FDA-approved targeted therapy (no off-label).
- [ ] Chondrosarcoma IDH BMAs cite trial data (not solid evidence yet).

## Rejection Criteria

- Off-label recommendations.
- Tier inflation.

## Claim Method

`formal-issue`
