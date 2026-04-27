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
- **Economic Profile** (NEW — see §"Economic Profile" below; this is a hard gate, not a formality)
- **Compute Classification** (NEW — `mechanical` / `llm-essential` / `mixed`)
- **Output Type** (NEW — `entity-sidecar` / `report-only` / `mixed`)
- Safety checklist
- Acceptance criteria (machine-checkable + semantic)
- Rejection criteria
- Reviewer

## What a Chunk is

A Chunk is **one concrete and complete task that requires meaningful LLM compute** — semantic reading, synthesis, judgment, or evidence drafting. Mechanical work that a Python script can do should be a script, not a chunk.

One chunk = one contributor = one PR = one review.

## Economic Profile (the break-even gate)

**Chunks that fail the break-even test must not be opened as chunks.** If verification cost exceeds the value of contributor work, the chunk is a net-negative even when contributor tokens are free.

The economic value equation:

```
Chunk Net Value = (Contributor work value)
                - (Maintainer review hours × maintainer rate)
                - (Co-Lead review hours × Co-Lead rate)
                - (Pipeline ceremony cost: issue + PR + CI + comments)
                + (Token savings vs in-house execution)
```

Every chunk spec must declare:

```yaml
## Economic Profile

compute_profile: mechanical | llm-essential | mixed
llm_essential_pct: <0–100>          # honest estimate of work that genuinely needs LLM
script_alternative:
  exists: yes | no | partial
  path: scripts/foo.py | null       # if a script could replace
  rationale: >                      # one-paragraph: why script is/isn't sufficient

verification_method: automated | sample | full-expert-review | mixed
verification_cost:
  maintainer_hours: <number>        # estimated mechanical validation + sample review
  colead_hours: <number>            # estimated clinical signoff (0 for report-only chunks)
  expert_specialty: ""              # e.g. "Ukrainian-fluent clinician" if needed

break_even_test: PASS | MARGINAL | FAIL
break_even_rationale: >             # one paragraph: how the chunk earns its keep
```

**Decision rules:**

- `break_even_test: PASS` — open the chunk.
- `break_even_test: MARGINAL` — open the chunk but track actual review hours; if exceeded, downgrade to FAIL.
- `break_even_test: FAIL` — **do not open**. Either:
  - Write a script (`scripts/foo.py`) and run it as a maintainer task.
  - Defer until economics improve (e.g. partial automation appears, or expert review becomes cheaper).
  - Drop the work scope.

A chunk MARKED FAIL on its spec page should remain visible as a "considered, declined" entry — institutional memory prevents re-proposal.

## Compute Classification

`compute_profile`:

- **mechanical** — work that a Python script with access to the repo + standard libraries could do equivalently. LLM is being used because nobody wrote the script, not because it's needed. **Default response: write the script.**
- **llm-essential** — work requires semantic NLU, synthesis from multi-source narrative, judgment, bilingual review, or other LLM-only capability. **Open as chunk.**
- **mixed** — partial mechanical (regex / scrape / parse) + partial semantic. **Decide based on `llm_essential_pct`:** ≥ 50% → chunk; < 50% → script + selective LLM step.

`llm_essential_pct` is an honest estimate: of the work to be done, what percentage genuinely needs LLM? If you can't articulate the percentage, you haven't thought about it enough.

## Output Type

`output_type`:

- **entity-sidecar** — sidecars target specific entities for upsert into hosted content. Validator routes target_action gates here.
- **report-only** — sidecars are reports / audits / findings. No upsert path. Validator skips target_action requirement.
- **mixed** — chunk produces both entity-sidecars and report-only files (e.g. drafts + a wrap-up report).

The validator uses `output_type` to route gates (target_action requirement, banned-source check, manifest-scope check).

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
