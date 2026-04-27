# MVP Roadmap

## Phase 0: Discovery

Define TaskTorrent concepts, safety boundaries, initial project categories, maintainer needs, and the first OpenOnco demand queue.

Deliverables:

- Planning repository
- Initial docs
- Draft chunk format
- Draft skill specs
- GitHub issue and PR templates

## Phase 1: Manual Chunks

Publish manually written chunk specs. Contributors select active chunks manually and submit outputs through GitHub.

Deliverables:

- First OpenOnco chunks (active subset of `chunks/openonco/`)
- Stable chunk IDs and disjoint manifests
- Manual review instructions
- Maintainer-owned acceptance criteria
- Per-chunk re-verification spec (compute + sample threshold)

## Phase 2: GitHub Workflow

Use GitHub issues, pull requests, labels, and templates as the primary execution workflow.

Deliverables:

- Chunk Task issue template
- Pull request template
- Topic labels (`civic-evidence`, `citation-verify`, `audit`, `ua-translate`, `evidence-draft`, `source-ingest`)
- Status labels (`status-active`, `status-in-review`, `status-closed`)
- Review checklist

## Phase 3: Validation Automation

Add lightweight validation for structured outputs. This may include schema checks, broken-link checks, required-field checks, manifest-overlap detection, and banned-source blocking.

Deliverables:

- Output schemas
- Validation scripts or actions
- Citation link checks
- Manifest-overlap checker (blocks opening a new active chunk that collides with a currently-active one)
- AI-tool / AI-model metadata audit script

## Phase 4: Contributor Dashboard

Create a dashboard that helps contributors enter capacity, choose preferred pace, view demand queues, and select chunks.

Deliverables:

- Capacity-to-Drop estimator
- Chunk recommendations by topic label
- Chunk status view
- Contributor history

## Phase 5: API And Automation Later

Add API and deeper automation only after the manual workflow is validated. Automation should support review, routing, and validation, not bypass maintainer approval.

Deliverables:

- Project demand API
- Chunk registry
- Tool integrations
- Automated status sync
