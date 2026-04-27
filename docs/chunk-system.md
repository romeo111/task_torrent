# Chunk System

## Help Chunk And Chunk Model

A Help Chunk is a public request for structured AI-assisted help on a single coherent task. A Chunk spec is the standardized form of that request.

In the MVP, every Chunk spec must include:

- Chunk ID (stable, kebab-case, project-scoped — e.g. `civic-bma-reconstruct-nsclc`)
- Project
- Mission
- Drop estimate
- Required skill
- Manifest (entities, files, or rows in scope)
- Allowed sources
- Output format (sidecar paths, report shape)
- Safety checklist
- Acceptance criteria (machine-checkable + semantic)
- Rejection criteria
- Reviewer

## What a Chunk is

A Chunk is **one concrete and complete task that requires meaningful LLM compute** — semantic reading, synthesis, judgment, or evidence drafting. Mechanical work that a Python script can do should be a script, not a chunk.

One chunk = one contributor = one PR = one review.

## Chunk Size

Chunk size follows the work, not a fixed slot. Examples:

- 0.1 Drop: small audit / wording review / format normalization (~10–20 entities)
- 0.5–1 Drop: typical evidence drafting / citation verification batch
- 1.5–3 Drop: tumor-wide BMA reconstruction or new-entity drafting batch

A chunk too large for one contributor to complete in one sitting should be split into named, independent chunks — not "subdivided into chunklets". Splitting must produce **disjoint manifests** so each result is independently reviewable.

## Manifest

Each chunk's manifest is the explicit, complete list of stable entity IDs (or file ranges, or claim triples) the chunk owns. Contributors must submit a `task_manifest.txt` matching the issue's manifest verbatim.

Outputs targeting entities outside the manifest are auto-rejected.

Manifests across **active** chunks must be disjoint. The maintainer who opens a chunk-task issue is responsible for checking against currently-open manifests. (See `openonco-pilot-workflow.md` §"File-set partitioning" for the OpenOnco rule.)

## Stable IDs

Chunks, entities, claims, citations, and output rows use stable IDs. Stable IDs make duplicate detection, review, and incremental updates tractable.

## Upsert Model

Outputs are designed as upserts, not blind replacements. A submitted row or structured object either creates a new item or updates the matching stable ID.

Sidecar payloads carry a `_contribution.target_action` of `new` | `upsert` | `flag_duplicate`.

## Isolated PRs

Contributors submit one PR per chunk. PRs do not bundle unrelated cleanup, formatting, or broad rewrites. The branch name is `tasktorrent/<chunk-id>` (project-scoped if needed).

## Duplicate Detection

Maintainers compare incoming outputs against existing stable IDs and normalized fields. Duplicates are merged, rejected, or flagged as alternate evidence — never silently added.

## Review Boundary

AI-generated outputs are drafts until reviewed. Maintainers decide whether output is accepted, revised, merged, or rejected. Project safety rules (e.g. OpenOnco's two-Clinical-Co-Lead signoff for hosted clinical content) layer on top.

## Topic Labels (replaces "Pack")

Earlier drafts of TaskTorrent had a `Pack` layer between Project and Chunk. That layer is gone. Topical grouping is done via GitHub labels on chunk-task issues:

- `civic-evidence` — CIViC-based evidence reconstruction
- `citation-verify` — citation verification reports
- `evidence-draft` — drafting new BMA / Indication / Drug entities
- `audit` — wording / format / consistency audits
- `ua-translate` — Ukrainian translation review
- `source-ingest` — Source stub drafting
- `dataset-normalize` — dataset cleanup with deterministic acceptance

A "shelf" is just a filtered query (`label:civic-evidence label:status-active`).

## Active vs Queued

- **Active chunks** have an open `[Chunk]` issue with `status-active` label. Contributors can claim them.
- **Queued chunks** have a chunk spec in `chunks/<project>/` but no open issue. They appear on the shelf but are not yet claimable.

Maintainers cap active count to fit review throughput. Default for OpenOnco pilot: 5 active chunks. See `openonco-pilot-workflow.md`.
