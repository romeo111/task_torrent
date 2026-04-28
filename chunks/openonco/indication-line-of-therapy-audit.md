# Chunk: indication-line-of-therapy-audit

## Status

`queued`

## Topic Labels

`audit`, `claim-bearing-review`, `indication-consistency`

## Mission

For ~250 hosted `Indication` (IND-*) entities, audit whether `applicable_to.line_of_therapy` (1, 2, 3, ...) matches what the cited primary_sources actually attest. Common drift mode: source attests "first-line" or "after platinum failure" but the Indication has been authored with a numerically-different line.

Report-only audit. No hosted-content edits. Drives maintainer-led IND-* corrections via standard CHARTER §6.1 flow.

## Economic Profile

```yaml
compute_profile: llm-essential
llm_essential_pct: 75
script_alternative:
  exists: no
  path: null
  rationale: >
    Reading source description of clinical context ("first-line",
    "platinum-resistant", "post-osimertinib") and matching against
    Indication's numerical line_of_therapy field is semantic NLU.
    String-match scripts catch "1L"/"first-line" but miss "platinum-
    pretreated" → 2L+ inference. LLM-essential.

verification_method: sample
verification_cost:
  maintainer_hours: 3
  expert_hours: 2     # 10% sample on flagged inconsistencies
  expert_specialty: "oncology"

break_even_test: PASS
break_even_rationale: >
  Manual line-of-therapy audit: ~5 min/Indication × 250 = 21 hours
  expert time. Contributor LLM at ~2k tokens × 250 = ~500k tokens.
  Sample-verify 5 hours total. Net: ~16 hours expert saved.

compute_classification: llm-essential
output_type: report-only
```

## Drop Estimate

~5 Drops (~500k tokens). 250 Indications × ~2k tokens per (read source description + check against line_of_therapy + write rationale).

## Required Skill

`drug-evidence-mapping` (audit mode).

## Allowed Sources

Hosted Indication YAMLs + their cited Source entities. Web access for source PDFs / abstracts.

## Manifest

All 250+ IND-* entities in `cancer-autoresearch/knowledge_base/hosted/content/indications/`.

## Computation

For each Indication:

1. Read `applicable_to.line_of_therapy` (numeric).
2. For each entry in `sources` (Citation objects), fetch `Source.url` if reachable; read the cited section.
3. Determine source-attested line context:
   - "first-line" / "1L" / "treatment-naive" → 1
   - "second-line" / "2L" / "after first-line failure" / "post-platinum" → 2
   - "third-line" / "3L" / "heavily pretreated" → 3+
   - "regardless of line" / "any line" / context-unclear → null
4. Compare numeric `line_of_therapy` vs source-attested:
   - `match` — agree
   - `mismatch` — clearly different
   - `ambiguous_source` — source doesn't specify line clearly
   - `over-restrictive` — Indication is more specific than source supports
   - `under-restrictive` — Indication is broader than source supports
5. Severity: `critical` (mismatch by ≥ 2 lines), `moderate` (1 line off), `minor` (over/under-restrictive but plausible).
6. Write rationale with quoted source phrase.

## Where computation happens

Contributor's machine. Web access for source content reading.

## Re-verification

### Pre-acceptance gates

- Schema validation on report.
- Every IND-* ID exists.
- Every row has rationale ≥ 100 chars + quoted source text on mismatch findings.
- `_contribution.ai_tool` + `ai_model` present.

### Computational re-verify

For `mismatch` rows: re-fetch the cited source and check the quote pattern in rationale appears in the source text. Flag if quote not present.

### Sample human re-verify

- Maintainer 10% (~25 IND): confirm category tags are reasonable.
- Co-Lead/oncologist 5% (~12 IND) on `mismatch` and `over-restrictive` subset: confirm clinical interpretation.

### Trust threshold

- Maintainer agreement ≥ 85%.
- Co-Lead/oncologist agreement on flagged subset ≥ 85%.

## Output Format

`contributions/indication-line-of-therapy-audit/audit-report.yaml`:

```yaml
findings:
  - finding_id: LOT-001
    ind_id: IND-NSCLC-2L-EGFR-T790M-OSIMERTINIB
    ind_file: knowledge_base/hosted/content/indications/...
    assigned_line: 2
    source_attested_line: 2
    finding_category: match
    severity: minor
    quoted_source_phrase: "...for treatment of patients with EGFR T790M-positive NSCLC who have progressed on or after EGFR-TKI therapy..."
    source_id: SRC-NCCN-NSCLC-2025
    verified_rationale: >
      NCCN NSCLC v3.2025 §EGFR-Subsequent-Therapy explicitly names
      osimertinib for post-1L EGFR-TKI failure (2L). Indication's
      line_of_therapy=2 matches.
    suggested_action: keep
```

Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- Gates pass.
- Sample agreement ≥ 85%.

## Rejection Criteria

- Mismatch flagged without quoted source phrase.
- Recommendation wording.
- Hosted-content edits.

## Reviewer

- Maintainer: 1 (10% sample).
- Oncologist: 1 (5% sample on mismatch subset).
