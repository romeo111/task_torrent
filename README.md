# TaskTorrent

TaskTorrent is a planning project for distributing structured AI work across many contributors. It helps social, research, and open-source projects break useful work into standardized tasks that people can run with their own AI tools.

## Core Idea

Many people have unused capacity in tools like Claude Code, Codex, Cursor, or ChatGPT. TaskTorrent turns that capacity into coordinated project work by publishing clear tasks with explicit scope, output format, safety rules, and review expectations.

## What Is A Drop?

1 Drop is an effort measurement unit equal to about 100k tokens of structured AI work. A Drop is not money, crypto, a credit, or a transferable asset. It only describes estimated AI work capacity.

## Chunks (Tasks)

The unit of work is a **Chunk** — a single, complete, LLM-essential task that ships as one GitHub issue, one contributor, one PR. A chunk has:

- a stable chunk ID
- a manifest of entities or files it touches
- an output schema
- explicit acceptance and rejection criteria
- a Drop estimate sized to the actual work (no fixed slot, no minimum, no maximum)

Chunks are grouped by topic via GitHub labels (e.g. `civic-evidence`, `citation-verify`, `ua-translate`), not by hierarchical "Packs". A topic-shelf is a filtered view of open chunks.

## How Work Flows

Projects publish chunk specs in `chunks/<project>/`. Maintainers open a GitHub issue from the chunk-task template when a chunk becomes active. Contributors execute using their own AI tools and submit a sidecar PR. Maintainers review and merge.

## First Pilot: OpenOnco

OpenOnco is the first pilot case. Its chunks focus on biomarker evidence reconstruction, drug evidence drafting, citation verification, and dataset normalization. OpenOnco safety boundaries forbid medical advice, treatment recommendations, and patient-specific outputs.

- Pilot framing: [`docs/openonco-first-case.md`](docs/openonco-first-case.md)
- Operational rules (sidecar workflow, source allowlist, reviewer routing, machine-checkable acceptance criteria, active-chunk limit): [`docs/openonco-pilot-workflow.md`](docs/openonco-pilot-workflow.md)
- Chunk shelf: [`chunks/openonco/`](chunks/openonco/) — 20 chunks defined; active subset opens as GitHub issues per maintainer-set limit.

## General Platform

TaskTorrent is not limited to oncology. The same chunk-shelf model can support civic tech, public datasets, documentation, education, open research, and other public-interest projects.

## MVP Boundary

This repository is for planning only. It contains docs, chunk specs, skill specs, and GitHub templates. It does not include production app code, token transfer, or automation that publishes AI output without maintainer review.
