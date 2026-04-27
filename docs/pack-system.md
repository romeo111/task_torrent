# Pack System

## Help Pack And Drop Pack Model

A Help Pack is a public request for structured AI-assisted help. A Drop Pack is the standard 1 Drop version of that request.

In the MVP, every Drop Pack should include:

- Pack ID
- Project
- Mission
- Total Drop estimate
- Chunk list
- Required skills
- Input context
- Output format
- Sources allowed
- Safety checklist
- Reviewer or maintainer owner

## Pack Size

Each Drop Pack equals about 1 Drop, or roughly 100k tokens of structured AI effort.

Each pack should contain 4 to 6 Chunks. Each Chunk should usually be about 0.15 to 0.3 Drop.

## Chunk Design

Chunks should be independently executable and independently reviewable. A contributor should understand what to do, what not to do, and what to submit without needing private maintainer context.

Each Chunk should include:

- Stable chunk ID
- Objective
- Scope boundaries
- Drop estimate
- Required skill
- Output schema
- Acceptance criteria
- Rejection criteria

## Overlap Compatibility

Packs must be overlap-compatible so multiple contributors can work in parallel without corrupting project state.

## Deterministic Scope

Each chunk needs a deterministic scope. The scope should define exactly which disease, biomarker, source set, page, dataset field, or citation range the contributor should touch.

## Stable IDs

Packs, chunks, entities, claims, citations, and output rows should use stable IDs where possible. Stable IDs make duplicate detection, review, and merge handling easier.

## Upsert Model

Outputs should be designed as upserts, not blind replacements. A submitted row or structured object should either create a new item or update the matching stable ID.

## Isolated PRs

Contributors should submit isolated pull requests for individual chunks or tightly related chunk groups. A PR should not bundle unrelated cleanup, formatting, or broad rewrites.

## Duplicate Detection

Maintainers should compare incoming outputs against existing IDs, names, links, and normalized fields. Duplicates should be merged, rejected, or marked as alternate evidence rather than silently added.

## Review Boundary

AI-generated outputs are drafts until reviewed. Maintainers decide whether output is accepted, revised, merged, or rejected.
