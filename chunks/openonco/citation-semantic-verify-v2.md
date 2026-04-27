# Chunk: citation-semantic-verify-v2

## Status

`queued` (proposed; supersedes citation-verify-914-audit which under-delivered scope)

## Topic Labels

`citation-verify`, `semantic-NLU`, `replaces-prior-chunk`

## Mission

For the 914 `(entity, claim, source)` findings already structured in `contributions/citation-verify-914-audit/citation-report.yaml` (PR #15), perform the **actual semantic source-by-source verification** that the prior chunk's scope-note explicitly skipped (`scope_note: It does not claim source-level verification for rows where the audit did not provide a concrete SRC-* source to resolve`). For each finding, fetch the cited source, read the relevant section, and replace `support_status: unclear` with a real verdict (`supported` / `unsupported` / `unclear` after-investigation / `broken_link` / `access_blocked`).

## Why a v2

The prior chunk (`citation-verify-914-audit`, merged via cancer-autoresearch PR #15) structured an existing audit into a machine-readable report. It did NOT actually read the cited sources — `support_status: unclear` was assigned to all 914 rows by definition. This is a useful triage matrix but does not deliver verification.

Retroactive economic-profile assessment: prior chunk graded `PASS` based on assumed semantic NLU; actual delivery was ~30% LLM-essential (parse + structure) + 0% verification. Net value = triage matrix. **This v2 chunk delivers the actually-promised verification on top of the existing structured findings.**

## Drop Estimate

~12 Drops (~1.2M tokens). 914 rows × ~1.3k tokens average per row (resolve `SRC-*` → URL/DOI, fetch source content, read in light of claim, write rationale with locator quote, decide `support_status` + `suggested_action`).

## Required Skill

`citation-verification` (the original skill spec applies; this chunk is the "do it for real" iteration).

## Allowed Sources

The pilot allowlist per `docs/openonco-pilot-workflow.md` §"Source allowlist". Web access required. NCCN content checked **by reference only** (verify section locator exists in cited NCCN version, not the textual content).

## Manifest

The 914 `finding_id` values from `contributions/citation-verify-914-audit/citation-report.yaml`. Maintainer commits `task_manifest.txt` listing all 914 finding IDs.

For each finding, contributor reads:
- `entity_id`, `entity_file`, `claim_locator` — what's being claimed and where in the repo
- `source_id` (may be null), `source_section` (may be null), `audit_finding_type`
- `finding_text` — the original audit's description
- The cited source itself (web fetch or repo file resolution)

## Computation

For each finding:

1. **Resolve source.**
   - If `source_id` is set, look up `Source.url` on `cancer-autoresearch/main`.
   - If `source_id` is null but `audit_finding_type` is `missing-regulatory-source` / `missing-trial-source`, the chunk's job is to **find** a candidate Source by scanning the entity's text (drug names, trial names) and proposing a `SRC-*` (existing) or `source_stub.yaml` (new).
   - If unresolvable, mark `support_status: maintainer_review_needed_no_source`.

2. **Fetch source content.**
   - PubMed abstract / PMC OA full-text / CIViC EID page / openFDA JSON / DailyMed / NCCN section reference / ESMO/ASCO open guideline.
   - Banned sources stay banned.

3. **Read the cited section in light of the entity's claim.**
   - Open the entity YAML at `entity_file`, locate the field at `claim_locator`.
   - Compare the claim wording against the source content.

4. **Decide `support_status`:**
   - `supported` — source text directly attests claim. Quote section/page locator in `rationale`.
   - `unclear` — partial / topic-adjacent (genuine post-investigation, not the prior chunk's blanket-unclear).
   - `unsupported` — source contradicts or is silent on the specific claim.
   - `broken_link` — URL doesn't resolve.
   - `access_blocked` — paywalled/banned and no abstract sufficient.

5. **Decide `suggested_action`:**
   - `keep` | `revise_claim` | `replace_source` | `maintainer_review` | `source_stub_needed`.

6. **Write per-row update** to a NEW report file `citation-report-v2.yaml`. Each row carries:
   - `finding_id` (matching v1 report)
   - `prior_status: unclear` (audit value)
   - `verified_status` (one of the 5 above)
   - `verified_rationale` (with quote/locator)
   - `verified_at` date
   - `verifier` (contributor)
   - `suggested_action` (post-verification)

The v2 report is additive to v1 — does NOT overwrite the v1 report; pairs by `finding_id`.

## Where computation happens

Contributor's machine. Required:
- Read access to `cancer-autoresearch` for `SRC-*` resolution + entity claim text + v1 report
- Web access for source fetches
- For NCCN: licensed copy or reference-only check

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation: every row has `finding_id`, `verified_status`, `verified_rationale`, `verified_at`, `verifier`, `suggested_action`.
- Every `finding_id` matches v1 report (no extras, no missing).
- Every `verified_status: supported` row has `verified_rationale` ≥ 100 chars AND contains a section/page locator pattern.
- Every `suggested_action: replace_source` has a target `SRC-*` ID that exists on `master` OR a `source_stub.yaml` in chunk dir.
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify

- Spot-check: for 50 random `verified_status: supported` rows, validator runs `httpx.head` on `Source.url` to confirm reachability. Failures → reject batch.
- For `source_id: SRC-CIVIC-EID-<n>`: confirm EID exists in local snapshot.

### Sample human re-verify (10%)

Maintainer reads ~91 random rows stratified across `verified_status`:
- `supported` — verify quoted locator exists at the source.
- `unsupported` — verify source genuinely doesn't attest.
- `unclear` post-investigation — confirm maintainer would also call unclear after reading.

### Trust threshold

- Pre-acceptance gates: 100% pass.
- Computational re-verify: 100% pass.
- Sample human re-verify: ≥ 90% maintainer agreement on `verified_status`.

Below 90% → reject batch and require re-execution by different model/contributor.

## Output Format

`contributions/citation-semantic-verify-v2/citation-report-v2.yaml` — single file, schema:

```yaml
_contribution:
  chunk_id: citation-semantic-verify-v2
  contributor: <github>
  submission_date: <YYYY-MM-DD>
  ai_tool: <tool>
  ai_model: <model>
  ai_model_version: ""
  ai_session_notes: ""
  notes_for_reviewer: ""

paired_with: contributions/citation-verify-914-audit/citation-report.yaml
verification_date: <YYYY-MM-DD>

rows:
  - finding_id: CV914-0001
    prior_status: unclear
    verified_status: supported
    verified_rationale: >
      NCCN NSCLC v3.2025 §EGFR-Subsequent-Therapy explicitly states
      "Osimertinib is preferred for EGFR T790M+ progression..." which
      directly attests the claim in BMA-EGFR-T790M-NSCLC.evidence_summary.
    verified_at: '2026-MM-DD'
    verifier: <github>
    suggested_action: keep
    notes: ""
```

Plus `task_manifest.txt` (914 finding IDs) and `_contribution_meta.yaml`.

## Acceptance Criteria

- All gates pass.
- Sample re-verify ≥ 90%.
- Output is paired correctly with v1 report (1:1 finding_id correspondence).

## Rejection Criteria

- Any `verified_status: supported` row without locator quote.
- Any `verified_status: supported` based on training-memory rather than fetched source content (heuristic flag: rationale lacks specific section/page text).
- Banned sources used.
- `finding_id` mismatch with v1 report.
- PR includes files outside `contributions/citation-semantic-verify-v2/`.

## Reviewer

- Maintainer: 1, at PR merge.
- No Clinical Co-Lead signoff for the report itself; subsequent maintainer-led edits to hosted content (acting on findings) follow CHARTER §6.1.

## Economic Profile

```yaml
compute_profile: llm-essential
llm_essential_pct: 75
script_alternative:
  exists: partial
  path: null
  rationale: >
    URL/EID resolution + reachability checks scriptable. Reading abstract
    + judging support is semantic NLU at scale; no script substitute.
    The prior v1 chunk attempted to deliver this and explicitly skipped
    it — confirming LLM-essential nature.

verification_method: sample
verification_cost:
  maintainer_hours: 3   # 10% sample (91 rows) at ~2 min average
  colead_hours: 0       # report-only
  expert_specialty: ""

break_even_test: PASS
break_even_rationale: >
  Per-row verification by hand would take maintainer ~20 minutes/row =
  300+ hours for 914 rows. Contributor LLM-substituted at ~1.3k tokens/row
  = ~1.2M tokens total. Sample 10% = 3 maintainer hours. Net win is
  ~290 maintainer-hours saved if quality holds at 90% sample agreement.

compute_classification: llm-essential
output_type: report-only
```

## Lesson encoded

This chunk exists because v1 (citation-verify-914-audit) **declared scope it didn't deliver**. The v2 spec explicitly:

1. References v1 by finding_id pairing — output is delta on top of v1, not replacement.
2. Names the specific gap (`prior_status: unclear` → `verified_status: <real>`).
3. Has explicit `verified_rationale` shape requirements that prevent training-memory hallucination (must contain locator/quote text).
4. Ships in the chunk shelf as a "redo with fidelity" — institutional memory of why v1 was insufficient.

Future chunk-spec authors: if your chunk's `scope_note` says "does not claim X-level verification", X-level verification is a separate chunk. Don't bundle.
