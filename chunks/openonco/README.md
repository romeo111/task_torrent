# OpenOnco Chunk Shelf

This directory holds chunk specs for the OpenOnco pilot. Each chunk is one concrete, complete, LLM-essential task — minimum size ~1M tokens (~10 Drops) per `docs/openonco-pilot-workflow.md`.

## Active-cap

At most **10 chunks** carry `status: active` (open `[Chunk]` issues) at any time during the pilot. (Raised from initial 2 after the first wave validated the pipeline.)

## Current shelf (~70 Drops total)

| Chunk | Status | Drops | Topic |
|---|---|---:|---|
| [`civic-bma-reconstruct-all`](civic-bma-reconstruct-all.md) | queued (proposed first active) | ~12 | civic-evidence, mechanical+judgment |
| [`citation-verify-914-audit`](citation-verify-914-audit.md) | queued (proposed second active) | ~10 | citation-verify, semantic-NLU |
| [`rec-wording-audit-claim-bearing`](rec-wording-audit-claim-bearing.md) | queued | ~10 | audit, semantic-NLU |
| [`ua-translation-review-batch`](ua-translation-review-batch.md) | queued | ~12 | ua-translate, bilingual-review |
| [`redflag-indication-coverage-fill`](redflag-indication-coverage-fill.md) | queued | ~15 | evidence-draft, claim-bearing |
| [`bma-drafting-gap-diseases`](bma-drafting-gap-diseases.md) | queued | ~15 | evidence-draft, claim-bearing |
| [`source-stub-ingest-batch`](source-stub-ingest-batch.md) | queued | ~10 | source-ingest, metadata-only |

Total: ~84 Drops across 7 chunks.

## How to promote a queued chunk to active

1. Confirm a slot is free (current active count < 2).
2. Confirm the chunk's manifest does not overlap with any currently-active chunk's manifest.
3. Open a new `[Chunk]` GitHub issue from the chunk-task template.
4. Commit the canonical `task_manifest.txt` content into the issue body.
5. Apply labels: `chunk-task`, `status-active`, plus topic labels (`civic-evidence`, `citation-verify`, etc.).

## Chunk lifecycle

`spec drafted (queued)` → `[Chunk] issue opened (status-active)` → `contributor claims (assignee set)` → `PR opened (status-in-review)` → `merged or rejected (status-closed)`.

A merged sidecar PR moves the actual sidecar payloads to `cancer-autoresearch/contributions/<chunk-id>/`, but does NOT modify `knowledge_base/hosted/content/`. Promotion to hosted content happens at the maintainer-run upsert step, which carries the CHARTER §6.1 two-Clinical-Co-Lead signoff for claim-bearing content.
