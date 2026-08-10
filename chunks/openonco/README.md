# OpenOnco Chunk Shelf

This directory holds chunk specs for the OpenOnco pilot. Each chunk is one concrete, complete, LLM-essential task — minimum size ~1M tokens (~10 Drops) per `docs/openonco-pilot-workflow.md`.

## Active-cap

At most **10 chunks** carry `status: active` (open `[Chunk]` issues) at any time during the pilot. (Raised from initial 2 after the first wave validated the pipeline.)

## Current shelf (~92 Drops total)

| Chunk | Status | Drops | Topic |
|---|---|---:|---|
| [`civic-bma-reconstruct-all`](civic-bma-reconstruct-all.md) | queued (proposed first active) | ~12 | civic-evidence, mechanical+judgment |
| [`citation-verify-914-audit`](citation-verify-914-audit.md) | queued (proposed second active) | ~10 | citation-verify, semantic-NLU |
| [`rec-wording-audit-claim-bearing`](rec-wording-audit-claim-bearing.md) | queued | ~10 | audit, semantic-NLU |
| [`ua-translation-review-batch`](ua-translation-review-batch.md) | queued | ~12 | ua-translate, bilingual-review |
| [`redflag-indication-coverage-fill`](redflag-indication-coverage-fill.md) | queued | ~15 | evidence-draft, claim-bearing |
| [`bma-drafting-gap-diseases`](bma-drafting-gap-diseases.md) | queued | ~15 | evidence-draft, claim-bearing |
| [`source-stub-ingest-batch`](source-stub-ingest-batch.md) | queued | ~10 | source-ingest, metadata-only |
| [`algo-branch-wiring-ovarian-2l`](algo-branch-wiring-ovarian-2l.md) | queued | ~1 | mechanical-rewrite, engine-wiring, algorithm-branch |
| [`algo-branch-wiring-breast-1l`](algo-branch-wiring-breast-1l.md) | queued | ~1 | mechanical-rewrite, engine-wiring, algorithm-branch |
| [`algo-branch-wiring-esoph-metastatic-1l`](algo-branch-wiring-esoph-metastatic-1l.md) | queued | ~1 | mechanical-rewrite, engine-wiring, algorithm-branch |
| [`workup-thyroid-papillary`](workup-thyroid-papillary.md) | queued | ~1 | evidence-draft, coverage-gap, diagnostic-workup |
| [`hereditary-brca-carrier-surveillance`](hereditary-brca-carrier-surveillance.md) | queued | ~2 | evidence-draft, coverage-gap, prevention, hereditary |
| [`prevention-regimen-authoring-wave1`](prevention-regimen-authoring-wave1.md) | queued | ~2-3 | evidence-draft, coverage-gap, prevention |

Total: ~92 Drops across 13 chunks.

## 2026-05-06 Expansion Shelf (300 Drops)

30 queued pieces, each sized at ~10 Drops (~1.0M tokens). These are intentionally queued; promote at most 10 to `status-active` at a time after manifest concretization and overlap checks.

| Chunk | Status | Drops | Topic |
|---|---|---:|---|
| [`openonco-shelf-zero-bma-apl-2026-05-06`](openonco-shelf-zero-bma-apl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-atll-2026-05-06`](openonco-shelf-zero-bma-atll-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-chondrosarcoma-2026-05-06`](openonco-shelf-zero-bma-chondrosarcoma-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-eatl-2026-05-06`](openonco-shelf-zero-bma-eatl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-lgg-2026-05-06`](openonco-shelf-zero-bma-lgg-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-hnscc-2026-05-06`](openonco-shelf-zero-bma-hnscc-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-hstcl-2026-05-06`](openonco-shelf-zero-bma-hstcl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-imt-2026-05-06`](openonco-shelf-zero-bma-imt-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-mf-sezary-2026-05-06`](openonco-shelf-zero-bma-mf-sezary-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-mpnst-2026-05-06`](openonco-shelf-zero-bma-mpnst-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-nk-t-nasal-2026-05-06`](openonco-shelf-zero-bma-nk-t-nasal-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-pmbcl-2026-05-06`](openonco-shelf-zero-bma-pmbcl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-ptcl-nos-2026-05-06`](openonco-shelf-zero-bma-ptcl-nos-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-zero-bma-t-pll-2026-05-06`](openonco-shelf-zero-bma-t-pll-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-burkitt-hcl-hcv-mzl-2026-05-06`](openonco-shelf-thin-bma-burkitt-hcl-hcv-mzl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-chl-ifs-mastocytosis-2026-05-06`](openonco-shelf-thin-bma-chl-ifs-mastocytosis-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-nlpbl-mzl-pcnsl-2026-05-06`](openonco-shelf-thin-bma-nlpbl-mzl-pcnsl-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-ptld-pv-sclc-2026-05-06`](openonco-shelf-thin-bma-ptld-pv-sclc-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-splenic-mzl-thyroid-atc-2026-05-06`](openonco-shelf-thin-bma-splenic-mzl-thyroid-atc-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-aitl-alcl-cervical-2026-05-06`](openonco-shelf-thin-bma-aitl-alcl-cervical-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-et-hgbl-mtc-2026-05-06`](openonco-shelf-thin-bma-et-hgbl-mtc-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-thin-bma-pmf-salivary-t-all-2026-05-06`](openonco-shelf-thin-bma-pmf-salivary-t-all-2026-05-06.md) | queued | ~10 | bma-drafting, coverage-gap |
| [`openonco-shelf-bma-civic-evidence-gap-wave3-a-2026-05-06`](openonco-shelf-bma-civic-evidence-gap-wave3-a-2026-05-06.md) | queued | ~10 | civic-evidence, citation-verify |
| [`openonco-shelf-bma-civic-evidence-gap-wave3-b-2026-05-06`](openonco-shelf-bma-civic-evidence-gap-wave3-b-2026-05-06.md) | queued | ~10 | civic-evidence, citation-verify |
| [`openonco-shelf-bma-civic-evidence-gap-wave3-c-2026-05-06`](openonco-shelf-bma-civic-evidence-gap-wave3-c-2026-05-06.md) | queued | ~10 | civic-evidence, citation-verify |
| [`openonco-shelf-bma-ua-signoff-prep-wave3-a-2026-05-06`](openonco-shelf-bma-ua-signoff-prep-wave3-a-2026-05-06.md) | queued | ~10 | ua-translate, clinical-review |
| [`openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06`](openonco-shelf-bma-ua-signoff-prep-wave3-b-2026-05-06.md) | queued | ~10 | ua-translate, clinical-review |
| [`openonco-shelf-source-license-recency-wave3-a-2026-05-06`](openonco-shelf-source-license-recency-wave3-a-2026-05-06.md) | queued | ~10 | source-ingest, recency |
| [`openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06`](openonco-shelf-drug-ua-nszu-access-wave3-a-2026-05-06.md) | queued | ~10 | access-audit, ua-context |
| [`openonco-shelf-regimen-evidence-source-trace-wave3-a-2026-05-06`](openonco-shelf-regimen-evidence-source-trace-wave3-a-2026-05-06.md) | queued | ~10 | citation-verify, regimen-audit |

Total: ~300 Drops across 30 queued pieces.

## How to promote a queued chunk to active

1. Confirm a slot is free (current active count < 2).
2. Confirm the chunk's manifest does not overlap with any currently-active chunk's manifest.
3. Open a new `[Chunk]` GitHub issue from the chunk-task template.
4. Commit the canonical `task_manifest.txt` content into the issue body.
5. Apply labels: `chunk-task`, `status-active`, plus topic labels (`civic-evidence`, `citation-verify`, etc.).

## Chunk lifecycle

`spec drafted (queued)` → `[Chunk] issue opened (status-active)` → `contributor claims (assignee set)` → `PR opened (status-in-review)` → `merged or rejected (status-closed)`.

A merged sidecar PR moves the actual sidecar payloads to `cancer-autoresearch/contributions/<chunk-id>/`, but does NOT modify `knowledge_base/hosted/content/`. Promotion to hosted content happens at the maintainer-run upsert step, which carries the CHARTER §6.1 two-Clinical-Co-Lead signoff for claim-bearing content.
