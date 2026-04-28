# Chunk: drug-class-normalization

## Status

`queued`

## Topic Labels

`audit`, `taxonomy-normalization`, `dataset-normalize`

## Mission

For ~216 hosted `Drug` entities, propose normalization of free-text `drug_class` field to a controlled vocabulary. The current `drug_class` is free-text (e.g., "EGFR tyrosine kinase inhibitor (3rd generation)", "anti-CD20 monoclonal antibody", "alkylating agent"). Inconsistent capitalization, generation-tagging, hyphenation. Maintainer-side render uses this field; consistency improves UX.

Report-only chunk: produces `drug_class_normalization_report.yaml` with per-Drug suggested controlled-vocab value. Maintainer applies suggestions per-row (no auto-apply per L-15 anti-pattern: contributor produces suggestions, maintainer reviews+applies).

## Economic Profile

```yaml
compute_profile: mixed
llm_essential_pct: 50
script_alternative:
  exists: partial
  path: null
  rationale: >
    50% mechanical: detect existing free-text patterns, group by
    similarity (string distance), propose canonical form. 50%
    LLM-essential: clinical domain judgment ("anti-CD20 monoclonal
    antibody" vs "anti-CD20 mAb" — same; "EGFR-TKI" vs "EGFR tyrosine
    kinase inhibitor" — same; "EGFR-TKI 3rd-gen" vs "EGFR-TKI 1st/2nd-gen"
    — different drugs in same class). Pure scripts produce
    over-collapsed clusters; LLM separates clinically distinct subclasses.

verification_method: full-maintainer-review
verification_cost:
  maintainer_hours: 4    # 100% review of suggestions before apply
  expert_hours: 0
  expert_specialty: ""

break_even_test: MARGINAL
break_even_rationale: >
  Manual drug_class normalization by maintainer: ~3 min/Drug × 216 =
  ~11 hours. Contributor LLM proposes; maintainer reviews each
  suggestion (~1 min each) = ~4 hours. Net: ~7 hours saved IF
  maintainer accepts ≥ 70% of suggestions. If accept rate drops below
  50%, suggestion overhead negates the saving.

  This is MARGINAL — track first-batch accept rate; if low, treat as
  FAIL for future taxonomy-normalization chunks. 100% maintainer
  review is mandatory: drug_class is rendered to clinicians and
  inconsistency is bad UX, but wrong canonicalization is worse.

compute_classification: mixed
output_type: report-only
```

## Drop Estimate

~3 Drops (~300k tokens). 216 Drugs × ~1k tokens per (read current drug_class + propose canonical + write rationale).

## Required Skill

`drug-evidence-mapping` (taxonomy mode).

## Allowed Sources

The hosted Drug entities + (optionally) ATC code lookups, RxNorm. No web fetch required for the normalization itself.

## Manifest

All 216+ DRUG-* entities in `cancer-autoresearch/knowledge_base/hosted/content/drugs/`.

## Computation

For each Drug:

1. Read current `drug_class` value (may be empty / free-text).
2. Read `mechanism`, `atc_code` for context.
3. Propose canonical drug_class form. Examples:
   - "EGFR tyrosine kinase inhibitor (3rd generation)" → canonical: "EGFR-TKI 3rd-generation"
   - "anti-CD20 monoclonal antibody" → canonical: "anti-CD20 mAb"
   - "" or null → propose based on mechanism + ATC
4. Tag finding:
   - `unchanged` — current value already canonical (no edit)
   - `whitespace_or_capitalization` — minor stylistic difference (low-stakes apply)
   - `generation_or_subclass_clarification` — adds 1st/2nd/3rd-gen tag, or "selective" / "covalent" qualifier
   - `class_change` — proposes a substantively different class (high-stakes; needs careful review)
   - `null_to_proposed` — current is null, propose new
5. Confidence: `high` / `medium` / `low`.
6. Write rationale.

## Where computation happens

Contributor's machine. Read-only access to cancer-autoresearch.

## Re-verification

### Pre-acceptance gates

- Schema validation on report.
- Every DRUG-* exists.
- Every `class_change` row has confidence >= medium and rationale ≥ 200 chars.
- `_contribution.ai_tool` + `ai_model` present.

### Computational re-verify

None. Domain-judgment work.

### Sample human re-verify (100% — full maintainer review)

This chunk explicitly does 100% maintainer review per Economic Profile (the suggestions are not auto-applied; maintainer walks the report row-by-row). The "verification" is merged with the application step.

### Trust threshold

- Accept rate ≥ 70% of suggestions on first batch. If below, reject batch + reconsider chunk economics.

## Output Format

`contributions/drug-class-normalization/drug_class_normalization_report.yaml`:

```yaml
findings:
  - drug_id: DRUG-OSIMERTINIB
    drug_file: knowledge_base/hosted/content/drugs/osimertinib.yaml
    current_drug_class: "EGFR tyrosine kinase inhibitor (3rd generation)"
    proposed_drug_class: "EGFR-TKI 3rd-generation"
    finding_category: generation_or_subclass_clarification
    confidence: high
    rationale: >
      Hyphenated abbreviation "EGFR-TKI" + numeric-then-suffix
      "3rd-generation" matches OpenOnco render style for sibling
      Drug entities (e.g., DRUG-LAZERTINIB also "3rd-generation").
      Mechanism field already says "3rd-generation EGFR-TKI", so
      drug_class becomes consistent with mechanism field.
```

Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- Gates pass.
- Maintainer accept rate ≥ 70% on first batch.

## Rejection Criteria

- Suggestions invent a class not supported by mechanism/ATC.
- High-confidence `class_change` without rationale.
- Hosted-content edits (this is report-only).

## Claim Method

`formal-issue` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1 (full review for application step).
- No Co-Lead unless `class_change` has clinical implications (rare for drug_class).

## Notes

This is the chunk to test "do MARGINAL chunks earn their keep?" If maintainer accept rate < 50%, future taxonomy-normalization chunks should be FAIL'd in Economic Profile and done as scripts + manual cleanup instead.
