# TaskTorrent

TaskTorrent is a planning project for distributing structured AI work across many contributors. It helps social, research, and open-source projects break useful work into standardized packages that people can run with their own AI tools.

## Core Idea

Many people have unused capacity in tools like Claude Code, Codex, Cursor, or ChatGPT. TaskTorrent turns that capacity into coordinated project work by publishing clear work units, expected outputs, review rules, and contribution paths.

## What Is A Drop?

1 Drop is an effort measurement unit equal to about 100k tokens of structured AI work. A Drop is not money, crypto, a credit, or a transferable asset. It only describes estimated AI work capacity.

## Drop Packs And Chunks

A Drop Pack is one complete work package worth about 1 Drop. Each Drop Pack is split into smaller Chunks, usually about 0.15 to 0.3 Drop, so contributors can choose work that matches their available time and AI capacity.

## How Work Flows

Projects publish Drop Packs. Contributors choose Chunks, execute them using their own AI tools, and submit outputs through GitHub pull requests or structured files. Maintainers review submitted work before anything is published or merged.

## First Pilot: OpenOnco

OpenOnco is the first pilot case. Its initial packs focus on biomarker evidence mapping, drug evidence mapping, citation verification, disease page improvement, and dataset normalization. OpenOnco work must avoid patient-specific advice and treatment recommendations.

- Pilot framing: [`docs/openonco-first-case.md`](docs/openonco-first-case.md)
- Operational rules (sidecar workflow, source allowlist, reviewer routing, machine-checkable acceptance criteria): [`docs/openonco-pilot-workflow.md`](docs/openonco-pilot-workflow.md)
- First pack: [`packs/openonco/civic-bma-reconstruction-1drop.md`](packs/openonco/civic-bma-reconstruction-1drop.md)

## General Platform

TaskTorrent is not limited to oncology. The same pack, chunk, skill, and review model can support civic tech, public datasets, documentation, education, open research, and other public-interest projects.

## MVP Boundary

This repository is for planning only. It contains docs, pack specs, skill specs, and GitHub templates. It does not include production app code, token transfer, or automation that publishes AI output without maintainer review.
