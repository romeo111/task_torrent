# Contributor Capacity Matching

This doc covers how a contributor selects a chunk that fits their tooling. In the current MVP, matching is manual: contributors browse the chunk shelf and self-select. This document describes the eventual matching model for Phase 4.

## Capacity inputs (eventual)

When a contributor signs up via the (future) dashboard, they provide:

- AI tool (Claude Code, Codex, Cursor, ChatGPT, other)
- Model in use (claude-opus-4-7, gpt-5-mini, etc.)
- Daily / weekly token budget (estimated)
- Topic preference (optional)
- Skill confidence (optional, e.g. "comfortable with citation verification but new to evidence drafting")

The goal is to estimate available Drop capacity, not to collect billing data.

## Capacity conversion

1 Drop ≈ 100k tokens of structured AI effort.

- 100k tokens/day ≈ 1 Drop/day
- 1M tokens/week ≈ 10 Drops/week
- 5M tokens/week ≈ 50 Drops/week (high-tier Pro contributor)

## Chunk-size policy

Chunks in TaskTorrent are minimum ~1M tokens (~10 Drops) to keep infrastructure overhead proportional to work value. A contributor whose weekly budget is < 10 Drops cannot complete a full chunk in one cycle.

Options for sub-chunk-sized contributors (Phase 4):

- Co-execution: pair with another contributor on the same chunk (one drafts, one reviews — both names on `_contribution.contributor`).
- Maintainer-curated mini-tasks: not yet defined; would require a different ceremony tier.

## Topic preference

Topic preferences match against chunk labels (`civic-evidence`, `citation-verify`, `audit`, `evidence-draft`, `ua-translate`, `source-ingest`). If multiple topic-matching chunks are active, the demand queue ranks by maintainer priority.

If no preference given, contributor sees all active chunks ordered by Drop estimate (smallest first) so they can pick what fits.

## Fast / Gradual mode

- **Fast mode** assigns the largest available chunk that fits the contributor's capacity.
- **Gradual mode** prefers chunks with `audit` or `report-only` labels (lower clinical risk) before claim-bearing work.

Both modes stay within the current active-chunk cap (2 in OpenOnco pilot).

## Manual selection (current MVP)

For the MVP no automated matching exists. Contributors:

1. Browse `chunks/<project>/` for spec.
2. Filter open `[Chunk]` issues by topic label.
3. Self-assign.
4. Open PR when done.

This is sufficient at pilot scale. Phase 4 brings automation when contributor count and chunk count make manual selection tedious.
