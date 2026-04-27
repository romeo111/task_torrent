# Product Vision

## Problem

Useful AI work is often limited by coordination rather than model capability. Social and open-source projects need research, cleanup, extraction, verification, documentation, and dataset work, but maintainers cannot reliably turn vague needs into safe, reviewable tasks for many contributors.

At the same time, many users have spare AI capacity in tools they already pay for or access. That capacity is hard to direct toward shared projects because tasks are not standardized, scopes overlap unpredictably, and outputs are difficult to review.

## Solution

TaskTorrent creates a planning and packaging layer for distributed AI work. Projects publish standardized Drop Packs that define mission, scope, chunks, required skills, output schema, safety rules, and review expectations.

Contributors pick chunks that match their available capacity, run the work with their own AI tools, and submit structured outputs through GitHub pull requests or files. Maintainers review, merge, reject, or request changes.

## Torrent Metaphor

TaskTorrent borrows the coordination metaphor from torrents, not the file-sharing mechanism. A large project need is split into smaller pieces, many contributors can work in parallel, and maintainers assemble useful reviewed outputs over time.

The key idea is swarm execution with structured review:

- Projects publish demand.
- Contributors bring local AI capacity.
- Packs define the work.
- Chunks make work parallel.
- Review keeps quality under maintainer control.

## Why Now

AI coding and research tools are widely available, but most projects still lack a practical way to absorb distributed AI labor. GitHub already provides issues, pull requests, reviews, files, history, and maintainer permissions. TaskTorrent can start as a lightweight repository standard before any production application exists.

## Long-Term Vision

TaskTorrent should become a general platform for matching project needs with contributor AI capacity. Over time it can support dashboards, validation automation, demand queues, contributor profiles, pack discovery, and API integrations.

The long-term goal is not autonomous publishing. It is a safer work distribution system where AI-assisted contributors produce structured drafts, maintainers retain authority, and useful public-interest projects get more help.
