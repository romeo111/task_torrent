# Product Vision

## Problem

Useful AI work is often limited by coordination rather than model capability. Social and open-source projects need research, cleanup, extraction, verification, documentation, and dataset work, but maintainers cannot reliably turn vague needs into safe, reviewable tasks for many contributors.

At the same time, many users have spare AI capacity in tools they already pay for or access. That capacity is hard to direct toward shared projects because tasks are not standardized, scopes overlap unpredictably, and outputs are difficult to review.

## Solution

TaskTorrent creates a planning and review layer for distributed AI work. Projects publish standardized **Chunks** — concrete, complete, LLM-essential tasks — that define mission, scope, manifest, output schema, allowed sources, and verification spec.

Contributors pick chunks that match their tooling, run the work with their own AI tools, and submit structured outputs through GitHub pull requests. Maintainers verify mechanically, sample-check semantically, and merge or reject.

## Torrent Metaphor

TaskTorrent borrows the coordination metaphor from torrents, not the file-sharing mechanism. A project's work surface is split into chunks; many contributors can work in parallel on different chunks; maintainers assemble useful reviewed outputs over time.

Key ideas:

- Projects publish demand as standardized chunk specs.
- Contributors bring local AI capacity.
- Chunks are the unit of dispatch.
- Manifests partition work so chunks are non-overlapping.
- Output-based verification keeps quality under maintainer control without requiring trust in the contributor's process.

## Why Now

AI coding and research tools are widely available, but most projects still lack a practical way to absorb distributed AI labor. GitHub already provides issues, pull requests, reviews, files, history, and maintainer permissions. TaskTorrent can start as a lightweight repository standard before any production application exists.

## Long-Term Vision

TaskTorrent should become a general platform for matching project needs with contributor AI capacity. Over time it can support dashboards, validation automation, demand queues, contributor profiles, chunk discovery, and API integrations.

The long-term goal is not autonomous publishing. It is a safer work distribution system where AI-assisted contributors produce structured drafts, maintainers retain authority, and useful public-interest projects get more help.
