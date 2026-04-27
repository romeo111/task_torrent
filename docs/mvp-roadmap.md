# MVP Roadmap

## Phase 0: Discovery

Define TaskTorrent concepts, safety boundaries, initial project categories, maintainer needs, and the first OpenOnco demand queue.

Deliverables:

- Planning repository
- Initial docs
- Draft pack format
- Draft skill specs
- GitHub issue and PR templates

## Phase 1: Manual Drop Packs

Publish manually written Drop Packs and Chunks. Contributors select work manually and submit outputs through GitHub.

Deliverables:

- First OpenOnco packs
- Stable chunk IDs
- Manual review instructions
- Maintainer-owned acceptance criteria

## Phase 2: GitHub Workflow

Use GitHub issues, pull requests, labels, and templates as the primary execution workflow.

Deliverables:

- Help Pack issue template
- Chunk Task issue template
- Pull request template
- Recommended labels
- Review checklist

## Phase 3: Validation Automation

Add lightweight validation for structured outputs. This may include schema checks, broken-link checks, required-field checks, and duplicate ID detection.

Deliverables:

- Output schemas
- Validation scripts or actions
- Citation link checks
- Duplicate detection reports

## Phase 4: Contributor Dashboard

Create a dashboard that helps contributors enter capacity, choose preferred pace, view demand queues, and select chunks.

Deliverables:

- Capacity-to-Drop estimator
- Pack recommendations
- Chunk status view
- Contributor history

## Phase 5: API And Automation Later

Add API and deeper automation only after the manual workflow is validated. Automation should support review, routing, and validation, not bypass maintainer approval.

Deliverables:

- Project demand API
- Pack registry
- Tool integrations
- Automated status sync
