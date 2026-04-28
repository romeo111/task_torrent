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
- **Claim Method** (NEW — see §"Claim Method" below)
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

## Claim Method

How does a contributor announce they're working on a chunk so two contributors don't duplicate work? Each chunk-spec declares one of two `claim_method` values.

### `formal-issue` (default for open contributors)

1. Contributor finds an open `[Chunk]` issue with `status-active` label and no `assignee`.
2. Comments: `I'd like to take this chunk.`
3. Maintainer assigns the issue (within 24h SLA — auto-released otherwise).
4. `assignee` field on the issue is the visible lock — other contributors see the issue is taken.
5. Contributor branches `tasktorrent/<chunk-id>` and submits PR.

### `trusted-agent-wip-branch-first` (for pre-authorized contributor agents)

1. Maintainer pre-authorizes the contributor (e.g. their own Codex or a known partner agent). No formal issue-claim ceremony.
2. Contributor **immediately pushes a minimal/empty WIP commit** to `tasktorrent/<chunk-id>` on origin BEFORE doing significant local work. This branch on origin = the visible lock.
3. Contributor completes work locally; force-push or new commits to same branch.
4. Opens PR when done.

The WIP-branch-first rule prevents the "invisible window" between local-work-start and first-push from causing two trusted agents to duplicate the chunk.

### Anti-pattern: claim without announcement

Working on a chunk locally for hours/days without (a) issue assignment, or (b) a WIP branch on origin = invisible work that risks duplication. Both `claim_method` paths exist specifically to make claim visible.

### Stale-claim auto-release

A chunk-task issue with `assignee` set + no commits to `tasktorrent/<chunk-id>` for 14 days = stale. Maintainer (or bot) drops the assignee + relabels the issue `status-active`. Stale claims unblock the slot.

### Cross-chunk manifest overlap

Before opening a new chunk-task issue, maintainer runs `check_manifest_overlap.py` against all currently-active chunks. Manifest overlap blocks the open. Without this check, two chunks with different IDs but overlapping entity scope can collide at integration.
