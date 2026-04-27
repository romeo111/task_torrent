# Skill: Biomarker Extraction

## Purpose

Draft structured `BiomarkerActionability` (BMA) and `Biomarker` candidates from maintainer-approved sources for OpenOnco maintainers to review. This is evidence drafting only — no medical advice, no treatment recommendation wording, no patient-specific output.

## Project Context

OpenOnco stores knowledge as YAML files validated by Pydantic schemas in `knowledge_base/schemas/`. Two entities are relevant for this skill:

- **`Biomarker`** (BIO-*) — gene/variant taxonomy. One row per biomarker, disease-agnostic.
- **`BiomarkerActionability`** (BMA-*) — `(biomarker, variant, disease)` triple → ESCAT actionability tier with per-source evidence references. **This is the primary output type for the OpenOnco pilot**, because the CIViC pivot (April 2026) flagged ~399 BMA files with `actionability_review_required: true` that need evidence reconstruction.

Schema sources of truth:

- `knowledge_base/schemas/biomarker_actionability.py` (`BiomarkerActionability`, `EvidenceSourceRef`, `RegulatoryApproval`)
- `knowledge_base/schemas/biomarker.py` (`Biomarker`, `ActionabilityLookupHint`, `BiomarkerExternalIDs`)

If the schema files change, they win. Don't invent fields.

## Input

The chunk issue gives you:

- **Pack ID + Chunk ID** (e.g. `openonco-civic-bma-reconstruction-c1`)
- **Chunk manifest** — the explicit list of BMA-* IDs (or BMA filename range) the chunk owns. You must not write outputs for entities outside this manifest.
- **Disease scope** (e.g. `DIS-NSCLC`)
- **Biomarker scope** (e.g. `BIO-EGFR-T790M`, or a gene-level scope like "all BIO-KRAS-*")
- **Allowed source list** — see `docs/openonco-pilot-workflow.md` §"Source allowlist"
- **Existing entity references** — paths or IDs of the BMA / Biomarker files the chunk should update or use as anchors

## Output Schema (BMA candidate)

Submit one YAML file per BMA candidate to `contributions/<pack-id>/<chunk-id>/bma_<biomarker>_<variant>_<disease>.yaml`. The file content mirrors the real `BiomarkerActionability` schema, plus a wrapper block that maintainers strip on merge:

```yaml
# wrapper — stripped on merge into knowledge_base/hosted/content/biomarker_actionability/
_contribution:
  pack_id: openonco-civic-bma-reconstruction-1drop
  chunk_id: openonco-civic-bma-reconstruction-c1
  contributor: github-username
  submission_date: "YYYY-MM-DD"
  target_action: upsert       # upsert | new | flag_duplicate
  target_entity_id: BMA-EGFR-T790M-NSCLC   # required for upsert/flag_duplicate
  duplicate_of: null          # set when target_action=flag_duplicate
  ai_tool: codex              # required: claude-code | codex | cursor | chatgpt | other
  ai_model: gpt-5-mini        # required: short model name (e.g. claude-opus-4-7, gpt-5-mini, gemini-2.5-pro)
  ai_model_version: "2026-03" # optional: snapshot/build/checkpoint string when known
  ai_session_notes: ""        # optional: free-form (e.g. "ran 3 retries; final accepted manually")
  notes_for_reviewer: "Reconstructed evidence_sources from CIViC EID12345; ESCAT tier unchanged."

# BMA payload — fields match knowledge_base/schemas/biomarker_actionability.py
id: BMA-EGFR-T790M-NSCLC
biomarker_id: BIO-EGFR-T790M
variant_qualifier: "T790M"
disease_id: DIS-NSCLC
escat_tier: "IA"               # IA | IB | IIA | IIB | IIIA | IIIB | IV | X
evidence_summary: >
  1–3 sentence neutral clinical interpretation. Describe what the
  source attests, not what a clinician should do.
regulatory_approval:
  fda: ["osimertinib — 2L EGFR T790M+ NSCLC (FDA approved 2017)"]
  ema: ["osimertinib — 2L EGFR T790M+ NSCLC (EMA approved)"]
  ukraine: []
recommended_combinations:
  - "osimertinib monotherapy"
contraindicated_monotherapy: []
primary_sources:
  - SRC-CIVIC                  # FK → existing Source entity, ≥1 required
  - SRC-NCCN-NSCLC-2025
evidence_sources:
  - source: SRC-CIVIC          # FK → Source entity (SRC-*)
    level: "A"                 # source-native level token, verbatim
    evidence_ids: ["EID12345"] # source-internal IDs (CIViC EID, etc.)
    direction: "supports"      # CIViC: supports | does_not_support | null
    significance: "sensitivity"
    note: null
last_verified: "YYYY-MM-DD"
actionability_review_required: false   # set true if you cannot mechanically reconstruct
notes: |
  Optional free-text note for maintainers. Cite source IDs; do not paraphrase
  clinical recommendations.
```

## Output Schema (Biomarker candidate)

Submit to `contributions/<pack-id>/<chunk-id>/bio_<biomarker_id>.yaml` when proposing a new or updated `Biomarker`:

```yaml
_contribution:
  pack_id: <pack>
  chunk_id: <chunk>
  contributor: github-username
  target_action: new | upsert
  target_entity_id: BIO-KRAS-G12C
  ai_tool: <tool>
  ai_model: <model>           # required
  ai_model_version: ""        # optional
  ai_session_notes: ""        # optional
  notes_for_reviewer: ""

id: BIO-KRAS-G12C
names:
  en: "KRAS G12C"
  uk: "KRAS G12C"
biomarker_type: gene_mutation
mutation_details:
  gene: KRAS
  gene_hugo_id: HGNC:6407
  exon: "2"
  variant_type: missense
  functional_impact: activating
  hgvs_protein: "p.G12C"
  hgvs_coding: "c.34G>T"
actionability_lookup:
  gene: KRAS
  variant: "G12C"
external_ids:
  hgnc_symbol: KRAS
  hgnc_id: "HGNC:6407"
  civic_id: "12"
  civic_url: "https://civicdb.org/genes/12"
  hgvs_protein: "p.G12C"
sources:
  - SRC-CIVIC
last_reviewed: "YYYY-MM-DD"
notes: ""
```

`actionability_lookup` and `oncokb_skip_reason` are mutually exclusive — set at most one. For IHC / score / serological / fusion-MVP / itd-MVP markers, set `oncokb_skip_reason` instead and leave `actionability_lookup` absent.

## Stable ID Rules

- BMA: `BMA-{biomarker}-{variant?}-{disease}` (e.g. `BMA-BRAF-V600E-CRC`).
- Biomarker: `BIO-{gene}-{variant?}` (e.g. `BIO-EGFR-T790M`, `BIO-KRAS-G12C`, `BIO-ALK-FUSION`).
- Source: pre-existing `SRC-*` entity. Do not invent. If the source you need has no `SRC-*` entry yet, submit a separate `source_stub.yaml` (see `skills/citation-verification.md` for the source-stub template) and set `_contribution.notes_for_reviewer` to flag the dependency.
- Disease: pre-existing `DIS-*` entity. Look up; do not invent.

## Rules

- Stay inside the chunk manifest. PRs that touch BMA-*/BIO-* IDs outside the manifest will be rejected.
- One BMA candidate = one file. No batch files.
- Every clinical claim in `evidence_summary`, `recommended_combinations`, `contraindicated_monotherapy`, and `notes` must be traceable to at least one entry in `primary_sources` or `evidence_sources`.
- Use neutral evidence wording: "source attests", "evidence supports", "CIViC reports". Do not write "patient should receive", "best treatment", "first choice".
- `evidence_sources[*].source` must reference a real `SRC-*` ID. If the source needs ingestion, file a `source_stub.yaml` in the same chunk directory.
- `evidence_sources[*].level` is the source-native token, verbatim (CIViC `A`/`B`/`C`/`D`/`E`; NCCN `Category 1`/`2A`; ESMO MCBS scores). Do not coerce levels across vocabularies.
- `escat_tier` follows ESMO ESCAT (Mateo et al. 2018, Ann Oncol 29:1895). If you cannot determine ESCAT mechanically from the cited evidence, set `actionability_review_required: true` and explain in `_contribution.notes_for_reviewer`.
- Never write `evidence_sources` entries with `source: SRC-ONCOKB` for new content — OncoKB is not an allowed source for the pilot. Pre-existing `SRC-ONCOKB` entries in the repo are legacy migration metadata; the render layer skips them.
- Flag duplicates with `target_action: flag_duplicate` and `duplicate_of: BMA-*`. Do not write near-identical BMA entries with different IDs.

## Good Output

A BMA file that:

- References an existing `BIO-*` and `DIS-*`.
- Has `evidence_sources` with at least one `SRC-CIVIC` entry carrying a real CIViC EID.
- Has `escat_tier` mapped from ESMO ESCAT criteria, not from the source-native level.
- Uses neutral wording in `evidence_summary`.
- Sets `actionability_review_required: false` only when the contributor genuinely cleared the migration flag.

## Bad Output

- `escat_tier: "best"` (not a valid token).
- `evidence_sources` empty while `actionability_review_required: false`.
- `evidence_summary: "Patients with T790M should be given osimertinib first-line."` (recommendation wording).
- Free-text source URL inside `primary_sources` instead of an `SRC-*` ID.
- BMA touching a disease outside the chunk manifest.
- A new `BIO-*` and a new `DIS-*` invented in the same submission.
