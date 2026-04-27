# OpenOnco Chunk Shelf

This directory holds chunk specs for the OpenOnco pilot. Each chunk is one concrete, complete, LLM-essential task — minimum size ~1M tokens (~10 Drops) per `docs/openonco-pilot-workflow.md`.

## Active-cap

At most **10 chunks** carry `status: active` (open `[Chunk]` issues) at any time during the pilot. (Raised from initial 2 after the first wave validated the pipeline.)

## Pilot status (post-first-wave)

All 7 initial chunks completed in 1 day. Retroactive Economic Profile per `docs/chunk-system.md` §"Economic Profile":

| Chunk | Status | Drops | Compute | Break-even | Lesson |
|---|---|---:|---|---|---|
| [`civic-bma-reconstruct-all`](civic-bma-reconstruct-all.md) | ✅ merged (PR #14) | ~12 | mechanical | **FAIL** | Should have been a script. ~1M tokens spent on what `scripts/reconstruct_bma_evidence_via_civic.py` does in minutes. **Do NOT re-open for additional tumor types.** |
| [`citation-verify-914-audit`](citation-verify-914-audit.md) | ✅ merged (PR #15) | ~10 | llm-essential (70%) | PASS | Clear win — semantic NLU at 914-row scale, 10% sample-verify. |
| [`rec-wording-audit-claim-bearing`](rec-wording-audit-claim-bearing.md) | ✅ merged (PR #17) | ~10 | mixed (70%) | PASS | Hybrid regex floor + LLM semantic catch in one pass. |
| [`ua-translation-review-batch`](ua-translation-review-batch.md) | ✅ merged (PR #17) | ~12 | llm-essential (70%) | PASS | Bilingual review — clear win, expensive verify (UA clinician). |
| [`bma-drafting-gap-diseases`](bma-drafting-gap-diseases.md) | ✅ merged (PR #21) | ~15 | llm-essential (70%) | MARGINAL | Net depends on Co-Lead accept-rate ≥ 70%. Track first batch. |
| [`redflag-indication-coverage-fill`](redflag-indication-coverage-fill.md) | ✅ merged (PR #21) | ~15 | llm-essential (80%) | MARGINAL | Higher stakes than bma-drafting (2-of-3 Co-Lead signoff). Track. |
| [`source-stub-ingest-batch`](source-stub-ingest-batch.md) | ✅ merged (PR #21) | ~10 | mixed (50%) | PASS | License-classification at scale; 20% sample-verify catches systematic errors. |

**Total: ~84 Drops contributor work, ~5 maintainer-fix PRs (validator gaps surfaced during review).**

## Pilot economic summary

- **1/7 chunks: FAIL** (civic-bma-reconstruct-all). Token cost was sunk; verification + upsert cost ~20 Co-Lead hours pending. **Net-negative if upsert proceeds.**
- **4/7 chunks: PASS.** Clear net-positive. These are the chunk archetypes to repeat.
- **2/7 chunks: MARGINAL.** Track Co-Lead accept-rate on first batch; re-classify after data.

## Lesson encoded

**Before opening any new chunk-task issue:** walk `docs/script-vs-chunk-decision.md`. Fill the chunk's Economic Profile honestly. If `break_even_test: FAIL`, write a script instead.

## How to promote a queued chunk to active

1. Confirm a slot is free (current active count < 10).
2. **Confirm `break_even_test: PASS` or MARGINAL with explicit budget.** FAIL chunks do not open.
3. Confirm the chunk's manifest does not overlap with any currently-active chunk's manifest.
4. Open a new `[Chunk]` GitHub issue from the chunk-task template.
5. Commit the canonical `task_manifest.txt` content into the issue body.
6. Apply labels: `chunk-task`, `status-active`, plus topic labels (`civic-evidence`, `citation-verify`, etc.).

## Chunk lifecycle

`spec drafted (queued)` → `economic profile filled` → `break_even_test: PASS or MARGINAL` → `[Chunk] issue opened (status-active)` → `contributor claims (assignee set)` → `PR opened (status-in-review)` → `merged or rejected (status-closed)` → `upsert applied (value realized)`.

A merged sidecar PR moves the actual sidecar payloads to `cancer-autoresearch/contributions/<chunk-id>/`, but does NOT modify `knowledge_base/hosted/content/`. Promotion to hosted content happens at the maintainer-run upsert step, which carries the CHARTER §6.1 two-Clinical-Co-Lead signoff for claim-bearing content.

**Track separately**: chunks that are `merged` (sidecars in repo) vs `applied` (upserted into hosted content). A merged-but-never-applied chunk has zero value realized.
