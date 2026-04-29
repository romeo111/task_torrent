# TaskTorrent

TaskTorrent is a coordination protocol for turning spare AI-agent capacity into
reviewable open-source work.

It helps a maintainer split a project into **Chunks**: scoped tasks with a
manifest, allowed sources, output format, safety rules, and acceptance criteria.
Contributors run those chunks with their own AI tools and submit pull requests.
Maintainers stay in control because every output is reviewed before it is
merged.

## v0.4 First Release

v0.4 is the first public TaskTorrent release. It is intentionally small:

- a reusable Chunk specification
- a cross-repo contract for consumer projects and contributor agents
- OpenOnco pilot chunks
- safety and review rules for high-stakes domains
- a lightweight linter and scaffold for projects that want code support
- a zero-code onboarding path for people who only want to prompt their agent

The release is not a hosted service, token system, marketplace, or autonomous
publishing bot. It is a GitHub-native protocol for organizing AI-assisted work
that still ends in human review.

## Install TaskTorrent With Zero Code

You do not need to install a package to use TaskTorrent. The simplest install is
to give your coding or research agent this prompt inside your project:

```text
You are helping me adopt TaskTorrent for this repository.

Read https://github.com/romeo111/task_torrent and use its v0.4 README,
docs/cross-repo-contract.md, docs/chunk-system.md, and relevant examples in
chunks/openonco/ as the protocol reference.

Do not write production code yet. First, propose a TaskTorrent integration plan
for this repository:

1. Identify 5-10 useful chunks of work that are safe for AI-assisted
   contributors.
2. For each chunk, define mission, manifest, allowed sources, disallowed
   sources, output format, acceptance criteria, rejection criteria, required
   skill, claim method, and Drop estimate.
3. Mark any safety boundaries or maintainer-review requirements.
4. Recommend which chunks should be opened first as GitHub issues.
5. Produce the first chunk spec in TaskTorrent v0.4 format.

Keep every chunk reviewable as one issue, one contributor, one branch, and one
pull request.
```

That is enough to start planning. If you later want local checks, install the
optional tooling:

```bash
pip install -e .
python -m tasktorrent.lint_chunk_spec --all chunks/
```

## How TaskTorrent Works

1. A project publishes chunk specs under `chunks/<project>/`.
2. Maintainers open active chunks as GitHub issues.
3. A contributor or agent claims one chunk.
4. Work lands in an isolated sidecar path in the consumer repo.
5. CI and maintainers verify the output.
6. The maintainer merges, rejects, or asks for revision.

The basic rule is: **one chunk = one contributor = one PR = one reviewable unit
of work**.

## What Is A Chunk?

A Chunk is a single, complete, LLM-essential task. A good chunk has:

- a stable chunk ID
- a concrete manifest of entities or files
- allowed and disallowed sources
- an output schema or file format
- machine-checkable acceptance criteria
- maintainer-checked semantic criteria
- explicit rejection criteria
- a claim method
- a Drop estimate

Chunks are grouped by GitHub labels and folders, not by heavyweight project
management layers.

## What Is A Drop?

A Drop is an approximate measure of AI work capacity. In this repository, 1 Drop
means about 100k tokens of structured AI-assisted work.

A Drop is not money, crypto, a credit, a reward, or a transferable asset. It is
only a planning estimate that helps maintainers size and compare chunks.

## First Work: OpenOnco

OpenOnco is the first TaskTorrent pilot. It is a strong first case because the
work is valuable, structured, citation-sensitive, and review-heavy.

The OpenOnco chunks focus on:

- biomarker evidence reconstruction
- drug evidence drafting
- citation verification
- Ukrainian translation review
- source-stub ingestion
- dataset normalization
- safety and red-flag coverage

OpenOnco also tests the parts of TaskTorrent that matter most: sidecar output,
source policy, reviewer routing, active-chunk limits, and output-based
verification. Its safety boundary is strict: TaskTorrent chunks must not produce
medical advice, treatment recommendations, or patient-specific outputs.

Start here:

- [OpenOnco first case](docs/openonco-first-case.md)
- [OpenOnco pilot workflow](docs/openonco-pilot-workflow.md)
- [OpenOnco chunk shelf](chunks/openonco/)

## Help Wanted

TaskTorrent needs two kinds of help.

If you maintain an open-source or public-interest project, try integrating
TaskTorrent. Ask your agent to draft a chunk shelf, open one small chunk as a
GitHub issue, and see whether the review loop works for your project.

If you want to contribute to OpenOnco, start by reading the OpenOnco pilot docs
and pick work that matches your skills: citation checking, structured data
cleanup, translation review, evidence mapping, or documentation.

Useful integrations include:

- project-specific chunk shelves
- issue templates for active chunks
- CI checks using the chunk-spec linter
- contributor quickstart docs
- sidecar validators for consumer repositories
- examples from domains outside oncology

## Optional Tooling

TaskTorrent v0.4 includes a lightweight Python package for projects that want
local validation:

```bash
pip install -e .
```

Commands:

- `tasktorrent-lint <chunk-spec.md>` validates a chunk spec.
- `tasktorrent-init <consumer-name>` scaffolds a basic consumer integration.

Run the linter against all chunks:

```bash
python -m tasktorrent.lint_chunk_spec --all chunks/
```

The tooling is useful, but it is not the product. The core product is the
protocol: clear chunks, safe boundaries, isolated outputs, and maintainer
review.

## Core Documents

- [Product vision](docs/product-vision.md)
- [Chunk system](docs/chunk-system.md)
- [Cross-repo contract](docs/cross-repo-contract.md)
- [Protocol v0.4 design](docs/protocol-v0.4-design.md)
- [Safety rules](docs/safety-rules.md)
- [OpenOnco pilot workflow](docs/openonco-pilot-workflow.md)

## Project Boundary

This repository contains the TaskTorrent protocol, docs, chunk specs, skill
specs, GitHub templates, and optional linter/scaffold tooling.

It does not contain a production web app, autonomous publication pipeline,
payment mechanism, token economy, or replacement for maintainer review.
