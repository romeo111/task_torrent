# Chunk: escat-tier-audit

## Status

`queued`

## Topic Labels

`audit`, `claim-bearing-review`, `escat`

## Mission

Audit `escat_tier` field across the 399 hosted `BiomarkerActionability` (BMA) entities. For each BMA, assess whether the assigned ESCAT tier is correctly mapped from the cited evidence per ESMO ESCAT criteria (Mateo et al. 2018 Ann Oncol 29(9):1895-1902). Flag overclaim (e.g., ESCAT IA on single-arm trial evidence) and underclaim (e.g., ESCAT IIIB when level-A guideline directly supports IA).

Output: `audit-report.yaml` with per-BMA assessment. **Report only — does not edit hosted content.** Findings drive subsequent maintainer-led BMA escat_tier corrections via the standard CHARTER §6.1 two-Co-Lead flow.

## Economic Profile

```yaml
compute_profile: llm-essential
llm_essential_pct: 80
script_alternative:
  exists: no
  path: null
  rationale: >
    ESCAT tier mapping requires reading evidence portfolio (RCT design,
    sample size, biomarker prevalence, disease setting) and applying
    Mateo et al. 2018 criteria. Pure judgment work — no script can do it.
    The 20% non-LLM portion is mechanical lookup of evidence_sources
    structure + checking presence of guideline references.

verification_method: sample
verification_cost:
  maintainer_hours: 4   # 10% sample (40 BMAs) at ~5 min average
  expert_hours: 2       # 5% Clinical Co-Lead sample on borderline calls
  expert_specialty: "oncology with ESCAT familiarity"

break_even_test: PASS
break_even_rationale: >
  Manual escat_tier audit by Co-Lead: ~10 min/BMA × 399 = 66+ hours.
  Contributor LLM at ~3k tokens/BMA × 399 = ~1.2M tokens. Sample-verify
  6 hours (maintainer + Co-Lead). Net win: ~60 Co-Lead hours saved.
  Quality risk: ESCAT criteria are well-defined; LLM should produce
  reliable judgments at sample-verify accuracy.

compute_classification: llm-essential
output_type: report-only
```

## Drop Estimate

~12 Drops (~1.2M tokens). 399 BMAs × ~3k tokens per (read evidence + map to ESCAT + write rationale).

## Required Skill

`biomarker-extraction` (in audit/judgment mode, not drafting).

## Allowed Sources

The hosted BMA entities themselves (read evidence_sources + primary_sources). The Mateo et al. 2018 ESCAT paper as the criteria reference (PMID 30137195). Pilot allowlist sources for cross-checking.

## Manifest

All 399 BMA entities in `cancer-autoresearch/knowledge_base/hosted/content/biomarker_actionability/`. Maintainer commits stable `BMA-*` IDs in `task_manifest.txt`.

## Computation

For each BMA:

1. Read entity's `escat_tier`, `evidence_sources`, `primary_sources`, `recommended_combinations`, `regulatory_approval`.
2. Map cited evidence to ESCAT criteria:
   - **IA**: prospective RCT (CIViC level A, NCCN cat 1, FDA-approved drug + CDx)
   - **IB**: retrospective evidence supporting biomarker selection
   - **IIA**: prospective basket trial
   - **IIB**: retrospective association from biomarker-driven trial
   - **IIIA**: case reports / case series with mechanistic plausibility
   - **IIIB**: pre-clinical evidence + biological rationale
   - **IV**: pre-clinical only
   - **X**: no evidence
3. Compare assigned `escat_tier` vs derived ESCAT tier.
4. Tag finding:
   - `correct` — agreed.
   - `overclaim` — assigned tier higher than evidence supports.
   - `underclaim` — assigned tier lower than evidence supports.
   - `borderline` — judgment call; document both sides.
   - `insufficient_evidence_to_audit` — evidence_sources is empty/sparse.
5. Severity: `critical` (overclaim by ≥ 2 tier levels e.g. IIIB→IA), `moderate` (1 tier off), `minor` (within-tier sub-distinction e.g. IA vs IB).
6. Write `verified_rationale` with explicit mapping: "evidence_sources contains CIViC level A + NCCN cat 1 → ESCAT IA per Mateo et al. §3.2".

## Where computation happens

Contributor's machine. Read access to cancer-autoresearch. Web access optional (for cross-checking against Mateo et al. paper, freely available via PubMed Central — open access).

## Re-verification

### Pre-acceptance gates

- Schema validation on `audit-report.yaml`.
- Every `BMA-*` ID exists on master.
- Every row has finding category + severity + rationale ≥ 100 chars.
- `_contribution.ai_tool` and `ai_model` present.

### Computational re-verify

None. ESCAT mapping is judgment-driven.

### Sample human re-verify

- Maintainer 10% sample (~40 BMAs) — confirm tier mapping is defensible.
- Clinical Co-Lead 5% sample (~20 BMAs) — focus on `borderline` and `overclaim` calls.

### Trust threshold

- Maintainer agreement ≥ 85% on tier calls.
- Co-Lead agreement ≥ 80% on borderline/overclaim subset (these are the high-stakes calls).

Below threshold → reject batch + re-run with different model/contributor.

## Output Format

`contributions/escat-tier-audit/audit-report.yaml`:

```yaml
_contribution:
  chunk_id: escat-tier-audit
  contributor: <github>
  ai_tool: <tool>
  ai_model: <model>
  ai_model_version: ""
  notes_for_reviewer: ""

findings:
  - finding_id: ESCAT-001
    bma_id: BMA-EGFR-T790M-NSCLC
    bma_file: knowledge_base/hosted/content/biomarker_actionability/bma_egfr_t790m_nsclc.yaml
    assigned_tier: IA
    derived_tier: IA
    finding_category: correct
    severity: minor
    confidence: high
    verified_rationale: >
      evidence_sources includes SRC-CIVIC level A (osimertinib sensitivity)
      + SRC-NCCN-NSCLC-2025 (cat 1 for T790M+) + FDA approval. Per Mateo
      et al. 2018 §3.2: ESCAT IA = prospective RCT or regulatory CDx
      driven biomarker selection. Both criteria satisfied. Tier IA correct.
    suggested_action: keep
```

Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- All gates pass.
- Sample re-verify thresholds met.
- Distribution of findings looks reasonable (e.g., not 100% "overclaim" — that'd suggest model bias).

## Rejection Criteria

- Tier judgments not grounded in cited evidence (LLM hallucination).
- Severity tags inconsistent (overclaim by 2 tiers tagged `minor`).
- Recommendation wording in `verified_rationale`.
- PR includes hosted content edits (this is report-only).

## Claim Method

`formal-issue` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1 (10% sample).
- Clinical Co-Lead: 1 (5% sample on overclaim/borderline subset).
