---
name: drug-evidence-mapping
description: Draft `Drug` (DRUG-*) and `Indication` (IND-*) sidecar candidates for OpenOnco maintainer review from manifest-owned entities only. Use when the user is on a chunk whose manifest includes drug or indication entities (regimen-outcome-fill, drug-class-normalization, redflag-indication-coverage-fill, etc.). Drafts only — neutral evidence wording, two-Clinical-Co-Lead signoff metadata required for claim-bearing fields, no treatment recommendations.
---

# Skill: Drug Evidence Mapping

## Purpose

Draft structured `Drug` and `Indication` candidates from maintainer-approved sources for OpenOnco maintainers to review. Evidence drafting only — no medical advice, no treatment selection, no patient-specific output.

## Project Context

OpenOnco's clinical recommendations are emitted by a declarative rule engine reading versioned YAML knowledge. Two entities matter for this skill:

- **`Drug`** (DRUG-*) — drug taxonomy: class, mechanism, regulatory status, AEs, dosing pointers.
- **`Indication`** (IND-*) — `(disease, line_of_therapy, biomarker_profile)` → recommended regimen with full provenance.

Schema sources of truth:

- `knowledge_base/schemas/drug.py`
- `knowledge_base/schemas/indication.py`
- `knowledge_base/schemas/regimen.py` (read for context; new Regimens are generally maintainer-authored, not contributor-drafted)

LLMs are not the clinical decision-maker (CHARTER §8.3). Contributors draft evidence rows; maintainers and Clinical Co-Leads decide what becomes a recommendation. Two-reviewer signoff (CHARTER §6.1) is required before any new Indication or BMA-bearing drug claim merges into `knowledge_base/hosted/content/`.

## Input

The chunk issue gives you:

- **Chunk ID**
- **Chunk manifest** — explicit DRUG-* / IND-* IDs (or a filename range) the chunk owns.
- **Disease scope** (e.g. `DIS-NSCLC`)
- **Drug scope** (e.g. specific DRUG-* IDs, a drug class, or a biomarker context like "EGFR-TKI 3rd-gen")
- **Allowed source list** — `docs/openonco-pilot-workflow.md` §"Source allowlist"
- **Existing entity references**

## Output Schema (Drug candidate)

Submit one YAML file per Drug candidate to `contributions/<chunk-id>/drug_<drug_id>.yaml`:

```yaml
_contribution:

  chunk_id: <chunk>
  contributor: github-username
  target_action: upsert | new
  target_entity_id: DRUG-OSIMERTINIB
  ai_tool: <tool>
  notes_for_reviewer: ""

id: DRUG-OSIMERTINIB
names:
  en: "osimertinib"
  uk: "осимертиніб"
atc_code: "L01EB04"
rxnorm_id: "1721560"
drug_class: "EGFR tyrosine kinase inhibitor (3rd generation)"
mechanism: >
  Irreversible EGFR-TKI selective for EGFR-activating mutations and the
  T790M resistance mutation.
regulatory_status:
  fda: "approved"
  ema: "approved"
  ukraine: "registered"
typical_dosing: "80 mg PO once daily"
formulations: ["80 mg tablet", "40 mg tablet"]
absolute_contraindications: []
black_box_warnings: []
major_interactions:
  - "Strong CYP3A4 inducers (rifampin, carbamazepine) — reduce osimertinib AUC"
common_adverse_events:
  - "Diarrhea"
  - "Rash"
serious_adverse_events:
  - "Interstitial lung disease"
  - "QT prolongation"
sources:
  - SRC-DAILYMED-OSIMERTINIB
  - SRC-FDA-LABEL-OSIMERTINIB
last_reviewed: "YYYY-MM-DD"
reviewers: []
notes: ""
notes_patient: null
```

## Output Schema (Indication candidate)

Indications are claim-bearing — they carry the actual treatment recommendation. Drafting an Indication is **higher-risk** than drafting a Drug or BMA. **For the pilot, Indication drafts must set `_contribution.target_action: new` and include explicit two-Clinical-Co-Lead-signoff flagging in `_contribution.notes_for_reviewer`.** Maintainers will not merge Indication drafts without two-Clinical-Co-Lead signoff (CHARTER §6.1).

Submit to `contributions/<chunk-id>/ind_<indication_id>.yaml`:

```yaml
_contribution:

  chunk_id: <chunk>
  contributor: github-username
  target_action: new | upsert
  target_entity_id: IND-NSCLC-2L-EGFR-T790M-OSIMERTINIB
  ai_tool: <tool>
  notes_for_reviewer: >
    Drafted from CIViC EID12345 + NCCN NSCLC v3.2025 §EGFR. ESCAT IA.
    Awaiting two Clinical Co-Lead signoffs per CHARTER §6.1.

id: IND-NSCLC-2L-EGFR-T790M-OSIMERTINIB
applicable_to:
  disease_id: DIS-NSCLC
  line_of_therapy: 2
  stage_requirements: ["IV"]
  biomarker_requirements_required:
    - biomarker_id: BIO-EGFR-T790M
      required: true
  biomarker_requirements_excluded: []
  demographic_constraints:
    ecog_max: 2
recommended_regimen: REG-OSIMERTINIB-MONO   # FK to existing Regimen
concurrent_therapy: []
followed_by: []
evidence_level: "1A"
strength_of_recommendation: "strong"
nccn_category: "1"
plan_track: "standard"
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: ["TEST-EGFR-NGS"]
desired_tests: []
rationale: >
  Source-attested neutral summary. Cite the source IDs that back the claim.
sources:
  - id: SRC-NCCN-NSCLC-2025
    section: "EGFR — Subsequent Therapy"
  - id: SRC-CIVIC
    evidence_id: "EID12345"
do_not_do:
  - "Do not switch to chemotherapy without confirming T790M status."
last_reviewed: "YYYY-MM-DD"
reviewers: []
notes: ""
```

## Stable ID Rules

- Drug: `DRUG-{INN}` uppercase (e.g. `DRUG-OSIMERTINIB`).
- Indication: `IND-{disease}-{line}-{biomarker_or_subset}-{regimen}`. Match neighboring IND-* files in the same disease for naming style.
- Regimen: `REG-*` — pre-existing entity. Do not draft new Regimens in the pilot; surface them as `_contribution.notes_for_reviewer: "needs new REG-*"`.
- Source: pre-existing `SRC-*`. Do not invent. File `source_stub.yaml` if needed (use the `source-stub-prep` skill in this plugin).

## Rules

- Stay inside the chunk manifest.
- One entity = one file.
- Use neutral wording: "evidence supports", "source attests", "guideline lists". Do not write "best treatment", "patients should receive", "first choice", "preferred over X".
- Every clinical claim must trace to at least one source citation.
- `nccn_category`, `evidence_level`, `strength_of_recommendation` come from the cited source — do not invent. If unclear, leave the field null and explain in `_contribution.notes_for_reviewer`.
- For Indication drafts, prefer `target_action: new` over editing existing IND-* files. Maintainers merge new drafts; they do not accept silent edits to existing Indications.
- Do not draft `recommended_regimen` for any disease/line/biomarker scenario unless the cited source explicitly attests that exact regimen.
- No OncoKB sources. Allowed sources are listed in `docs/openonco-pilot-workflow.md`.

## Good Output

- Drug file with `regulatory_status` strings copied verbatim from DailyMed/openFDA, plus `sources` listing the FDA label and DailyMed entry as `SRC-*` IDs.
- Indication file that names a `recommended_regimen: REG-*` only when the source explicitly attests that regimen for that exact `(disease, line, biomarker)` triple, with `evidence_level` and `nccn_category` lifted directly from the source.

## Bad Output

- `recommended_regimen: REG-OSIMERTINIB-MONO` for a scenario where the source describes EGFR-TKI as a class without naming osimertinib.
- `evidence_level: "1A"` without a source reference that attests level 1A.
- "Best treatment is osimertinib" anywhere in `evidence_summary`, `rationale`, or `notes`.
- `recommended_regimen: REG-NEW-REGIMEN-I-INVENTED`.
- A new Drug + new Indication + new Regimen all in one submission.
