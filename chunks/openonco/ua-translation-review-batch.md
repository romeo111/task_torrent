# Chunk: ua-translation-review-batch

## Status

`queued`

## Topic Labels

`ua-translate`, `bilingual-review`, `report-only`

## Mission

Review the ~1251 `*_ua` fields drafted by prior runs (most carry `ukrainian_drafted_by: claude_extraction` and `ukrainian_review_status: pending_clinical_signoff`). Identify (a) machine-translation artifacts, (b) calques/literal-translation problems, (c) clinical mistranslations, (d) untranslated English fragments inside `*_ua` text. Output: `audit-report.yaml` with per-field assessment and suggested corrections.

OpenOnco specs are in Ukrainian. Many entities have an English `evidence_summary` and a `evidence_summary_ua` companion that's a draft translation. Per `specs/CLINICAL_CONTENT_STANDARDS.md`, UA fields require Ukrainian-fluent clinician sign-off — but a contributor with strong UA + clinical reading can do the first pass.

## Drop Estimate

~12 Drops (~1.2M tokens). 1251 fields × ~1k tokens (read EN + UA, judge, write rationale + correction).

## Required Skill

Bilingual review (no formal skill spec yet — covered by output schema below). **Required: native-or-near-native Ukrainian + working medical English.**

## Allowed Sources

None. This chunk compares EN vs UA pairs within the OpenOnco repo only.

## Manifest

All entity files matching `ukrainian_review_status: pending_clinical_signoff` on `cancer-autoresearch/main`. Distribution likely:

- BMA `evidence_summary_ua`: ~399
- BMA `notes_ua` (if present): ~50
- RedFlag `description_ua`, `recommendation_ua`: ~580
- Indication / Drug / Disease patient-mode UA: ~220

Maintainer commits the canonical `task_manifest.txt` (one `<entity_id>::<field_path>` per line) at chunk-issue open.

## Computation

For each `(entity_id, field_path)` in manifest:

1. **Read** EN field and corresponding UA field from the same entity.
2. **Compare**:
   - Coverage: does UA convey the same clinical content?
   - Terminology: are clinical terms standard Ukrainian medical Ukrainian (e.g. "осимертиніб", "плоскоклітинний", "немілкоклітинний")?
   - Calques: literal Russian/English structure transferred mechanically (e.g. "cancer патієнти" instead of "пацієнти з онкозахворюванням")?
   - Untranslated fragments: English words left inside UA text (a known regression pattern in current draft state).
   - Clinical fidelity: does UA accidentally narrow/broaden the claim?
3. **Tag findings** with category: `untranslated_fragment` | `calque` | `terminology` | `clinical_drift` | `coverage_loss` | `acceptable`.
4. **For non-acceptable findings**, propose corrected UA text.
5. **Severity**: `critical` (clinical drift), `moderate` (terminology / coverage loss), `minor` (style / calque).

## Where computation happens

Contributor's machine. Read-only access to `cancer-autoresearch`. No web access.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on `audit-report.yaml`.
- Every `(entity_id, field_path)` exists on `cancer-autoresearch/main`.
- Manifest covers exactly the listed pending-signoff fields.
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify

Limited mechanical check:

- **Untranslated-fragment auto-detect**: maintainer-run script searches each UA field for runs of ≥ 3 consecutive English-alphabet words (excluding drug INNs, gene symbols, `e.g.`, common abbreviations whitelist). Findings the contributor's report missed → reject batch.

The other categories (calque, clinical drift) are not mechanically detectable.

### Sample human re-verify (15%)

A Ukrainian-fluent clinician reads ~190 random findings:

- Confirm severity tag.
- Confirm suggested correction is fluent and clinically faithful.
- Confirm `acceptable` tags are actually acceptable (false negatives are worse than false positives here).

### Trust threshold

- Untranslated-fragment cross-check: 0 misses.
- Sample human re-verify: ≥ 85% Ukrainian-clinician agreement on severity and correction.
- Sample false-negative rate (`acceptable` flagged that shouldn't be): ≤ 5%.

## Output Format

`contributions/ua-translation-review-batch/audit-report.yaml`:

```yaml
_contribution:
  chunk_id: ua-translation-review-batch
  contributor: github-username
  ai_tool: <tool>
  ai_model: <model>
  ai_model_version: ""
  notes_for_reviewer: "Bilingual contributor: native UA + medical EN."

findings:
  - finding_id: f-0042
    entity_id: BMA-EGFR-T790M-NSCLC
    field_path: "evidence_summary_ua"
    en_excerpt: "EGFR T790M is the dominant acquired-resistance mechanism after 1st/2nd-gen EGFR-TKI."
    ua_excerpt: "EGFR T790M is the dominant набутий-resistance механізм after 1st/2nd-gen EGFR-TKI."
    category: untranslated_fragment
    severity: critical
    suggested_correction: "EGFR T790M — домінуючий механізм набутої резистентності після EGFR-ТКІ 1-го/2-го поколінь."
    notes: "About 70% of the source string remained in English."
```

## Acceptance Criteria

- Gates pass.
- Untranslated-fragment cross-check: 0 misses.
- Ukrainian-clinician sample re-verify ≥ 85%.

## Rejection Criteria

- Cross-check finds untranslated fragments not in report.
- High false-negative rate (`acceptable` tag on text with clear clinical drift).
- Suggested corrections introduce new clinical claims.

## Claim Method

`trusted-agent-wip-branch-first` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1.
- Ukrainian-fluent clinician: 1, on a sample of findings, before maintainer accepts the batch.

## Notes

This chunk is the foundation for an eventual maintainer-led upsert into hosted UA fields. The audit findings drive subsequent edits; those edits go through `specs/CLINICAL_CONTENT_STANDARDS.md` UA-review process.
