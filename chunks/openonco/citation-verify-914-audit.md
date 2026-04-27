# Chunk: citation-verify-914-audit

## Status

`queued` (proposed second active chunk)

## Topic Labels

`citation-verify`, `semantic-NLU`, `pilot-active`

## Mission

Verify support for all 914 `(entity, claim, source)` findings listed in `cancer-autoresearch/docs/reviews/citation-verification-2026-04-27.md`. Output: a single structured `citation-report.yaml` with one row per finding — `support_status`, `rationale`, `suggested_action`, source quote/locator. **No edits to hosted content.**

## Drop Estimate

~10 Drops (~1.0M tokens). 914 rows × ~1.1k tokens per row average (read source section, judge support, write rationale with locator).

## Required Skill

`citation-verification`

## Allowed Sources

The exhaustive source-allowlist in `docs/openonco-pilot-workflow.md` §"Source allowlist". Web access required for PubMed abstracts, CIViC EIDs, openFDA, DailyMed, ClinicalTrials.gov. NCCN guideline content checked **by reference only** — verify the section/page locator exists in the cited NCCN version, not the textual content (which is not redistributable).

## Manifest

The 914 rows from `docs/reviews/citation-verification-2026-04-27.md`, formatted as `(entity_id, claim_locator, source_id, source_section)` triples. Maintainer commits the canonical `task_manifest.txt` at chunk-issue open.

Distribution by source domain (approximate):

| Source domain | Rows |
|---|---:|
| `SRC-PMID-*` / `SRC-PMC-*` | ~280 |
| `SRC-CIVIC` / `SRC-CIVIC-EID-*` | ~210 |
| `SRC-NCCN-*` | ~180 |
| `SRC-DAILYMED-*` / `SRC-OPENFDA-*` / `SRC-FDA-LABEL-*` | ~120 |
| `SRC-ESMO-*` / `SRC-ASCO-*` / `SRC-WHO-*` / `SRC-MOZ-*` | ~80 |
| Other / unknown | ~44 |

## Computation

For each row in the manifest, the contributor's AI tool:

1. **Resolve source** — locate `SRC-*` entity on `main`, fetch `Source.url` or section locator.
2. **Fetch source content** — PubMed abstract / CIViC EID page / openFDA JSON / DailyMed entry / NCCN section reference.
3. **Read** the cited section in light of the claim.
4. **Judge support_status:**
   - `supported` — source text directly attests claim. Quote section/locator in `rationale`.
   - `unclear` — partial / topic-adjacent.
   - `unsupported` — source contradicts or is silent on the specific claim.
   - `broken_link` — URL doesn't resolve or `Source.superseded_by` points to missing entity.
   - `access_blocked` — paywalled/banned and no abstract-only authorization.
5. **Decide suggested_action:** `keep` | `revise_claim` | `replace_source` | `maintainer_review` | `source_stub_needed`.
6. **Write rationale** — ≥ 1 sentence with section/page locator (or, for `unsupported`/`broken_link`, the specific failure).
7. **Append row** to `citation-report.yaml`.

Token budget per row: ~1.1k including source fetch/read.

## Where computation happens

Contributor's machine. Required:

- Read access to `cancer-autoresearch` (for `SRC-*` resolution + claim text).
- Web access for PubMed/CIViC/openFDA/DailyMed.
- For NCCN: read access to the contributor's licensed NCCN copy if available; otherwise reference-only check (does the cited section locator exist in the version table-of-contents).

The contributor's tool is opaque to the maintainer. The output rows are the only audit artifact.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation: every row has `entity_id`, `claim_locator`, `source_id`, `support_status`, `rationale`, `suggested_action`, `accessed`.
- Every `entity_id` exists on `cancer-autoresearch/main`.
- Every `source_id` exists on `cancer-autoresearch/main`.
- Every `support_status: supported` row has `rationale` ≥ 100 characters AND contains a section/page locator pattern.
- Every `suggested_action: replace_source` has `suggested_replacement_source_id` ∈ existing `SRC-*` set.
- `task_manifest.txt` covers exactly the 914 rows of the audit (no missing, no extra).
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify (partial)

A maintainer-run script checks:

- `support_status: broken_link` rows: HTTP HEAD on `Source.url` confirms 4xx/5xx or DNS fail. False positives (link works) → reject row.
- `source_id: SRC-CIVIC-EID-<n>` rows: confirm `EID<n>` is in the local CIViC snapshot. If contributor cited a non-existent EID → reject row.
- Banned-source check: any row with `source_id: SRC-ONCOKB` and `support_status != access_blocked` → reject.

### Sample human re-verify (10%)

Maintainer reads a random sample of ~91 rows (10%), stratified across support_status values:

- `supported` rows: open the cited source, verify the quoted locator exists and the claim is attested.
- `unsupported` rows: open the cited source, verify it does not attest.
- `unclear` rows: confirm the maintainer would also call them unclear.

### Trust threshold

- Pre-acceptance gates: 100% pass required.
- Computational re-verify: 100% pass required.
- Sample human re-verify: ≥ 90% maintainer agreement. Below → reject batch and require re-execution by a different model/contributor.

## Output Format

Single file: `contributions/citation-verify-914-audit/citation-report.yaml`. Schema in `skills/citation-verification.md`.

Plus `task_manifest.txt` and `_contribution_meta.yaml`.

## Acceptance Criteria

- All pre-acceptance gates pass.
- Computational re-verify shows 100% agreement.
- Sample human re-verify ≥ 90%.
- Maintainer accepts the report as actionable.

The report's findings drive a separate, maintainer-led set of edits to hosted content — those edits go through standard CHARTER §6.1 two-Co-Lead signoff. This chunk does not produce hosted-content changes.

## Rejection Criteria

- Banned source treated as `supported` instead of `access_blocked`.
- `supported` rows without a locator in `rationale`.
- Replacement source field contains a URL or invented `SRC-*` ID.
- Rows checking triples not in the audit's 914 (out-of-manifest).
- Claim text rewritten inside `rationale`.

## Reviewer

- Maintainer: 1.
- No Clinical Co-Lead signoff required for the report. Subsequent maintainer edits to hosted content (acting on the report) follow CHARTER §6.1.
