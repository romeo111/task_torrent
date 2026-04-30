# TaskTorrent

TaskTorrent is a GitHub-native protocol for turning AI-agent time into
reviewable open-source pull requests.

The first pilot is cancer-research data work for
[OpenOnco](https://github.com/romeo111/OpenOnco), a free oncology clinical
decision-support knowledge base. TaskTorrent breaks that work into **Chunks**:
small, scoped tasks with a manifest, allowed sources, output format, safety
rules, and acceptance criteria. Contributors use their own AI tools to complete
one chunk at a time. Maintainers review every output before it is merged.

TaskTorrent is not a marketplace, token system, payment system, hosted bot, or
autonomous publishing pipeline. It is a coordination layer for human-reviewed
work.

## Current OpenOnco Metrics

Live counts and the full claimable-chunks list are on the
[TaskTorrent landing page](https://romeo111.github.io/task_torrent/),
regenerated every 4 hours from registered consumer repos. Headline metrics:

- Completed chunks (cumulative): see landing
- Sidecar submissions counted (lifetime): see landing
- Claimable chunks right now: see landing
- Estimated work surface: ~16M tokens

Active chunks may live in either `romeo111/task_torrent` or the
consumer repo (`romeo111/OpenOnco`), depending on the wave. The
landing page merges both. To filter directly on GitHub:
[chunk-task + status-active in task_torrent](https://github.com/romeo111/task_torrent/issues?q=is%3Aopen+label%3Achunk-task+label%3Astatus-active)
or [in OpenOnco](https://github.com/romeo111/OpenOnco/issues?q=is%3Aopen+label%3Achunk-task+label%3Astatus-active).

Live public metrics are published through the landing data files:

- [landing/metrics.json](landing/metrics.json)
- [landing/chunks.json](landing/chunks.json)
- [TaskTorrent landing page](https://romeo111.github.io/task_torrent/)

If claimable chunks are `0`, OpenOnco is between active waves. You can still
read the shelf, prepare your environment, or ask the maintainer to open the next
chunk.

## Contribute To Cancer Research

### Claude Code (recommended)

Install the `openonco-contributor` plugin:

```text
/plugin marketplace add https://github.com/romeo111/task_torrent
/plugin install openonco-contributor@tasktorrent
```

Then run `/openonco-contribute` from a local checkout of
`romeo111/OpenOnco`. The plugin picks one currently claimable chunk,
summarizes scope, drafts sidecars under `contributions/<chunk-id>/`,
runs validation, and stops after one PR.

Plugin source and docs: [plugins/openonco-contributor/](plugins/openonco-contributor/README.md).

### Other coding agents (Codex / Cursor / ChatGPT / etc.)

Use this prompt from a local checkout of `romeo111/OpenOnco`:

```text
You are helping me contribute one TaskTorrent chunk to OpenOnco cancer-research
data work.

Read these first:
- https://github.com/romeo111/task_torrent
- https://github.com/romeo111/task_torrent/blob/main/docs/openonco-pilot-workflow.md
- https://github.com/romeo111/task_torrent/tree/main/chunks/openonco
- https://github.com/romeo111/task_torrent/tree/main/plugins/openonco-contributor/skills
- https://github.com/romeo111/OpenOnco

Pick exactly one currently claimable OpenOnco chunk. If no chunk is claimable,
stop and report that the shelf is between waves.

Before writing files, summarize:
1. the chunk ID and GitHub issue,
2. the manifest you will own,
3. allowed sources and banned sources,
4. output path under contributions/<chunk-id>/,
5. validation commands you will run.

Rules:
- Work only under contributions/<chunk-id>/ unless the chunk explicitly says
  otherwise.
- Do not write treatment advice or patient-specific recommendations.
- Do not use OncoKB, SNOMED CT, MedDRA, or any banned source in the chunk.
- Do not use git add -A, git add ., or --no-verify.
- Open one pull request for one chunk, then stop.
```

The safest first contributions are citation verification, source-stub cleanup,
translation review, structured evidence mapping, and schema-safe sidecar data
work. Clinical content still requires OpenOnco maintainer and clinical lead
review.

## OpenOnco Claude Plugin Plans

TaskTorrent is planning two separate Claude plugin tracks for OpenOnco:

- **OpenOnco TaskTorrent Contributor**: a public-first plugin for volunteers
  who want to donate AI-agent time to citation verification, source-stub
  cleanup, biomarker evidence sidecars, and chunk readiness review.
- **OpenOnco Clinical Evidence Review Support**: a later, stricter plugin for
  clinicians and maintainers reviewing evidence provenance, citation support,
  and sidecar submissions. This track needs a stronger privacy posture and a
  hard no-PHI boundary before any directory submission.

The contributor plugin is the recommended first submission because it is
sidecar-only, review-gated, and not patient-specific. The clinical-review plugin
should remain separate so it can carry tighter privacy, support, refusal, and
human-review requirements.

Planning docs:

- [OpenOnco contributor plugin plan](docs/openonco-contributor-plugin-plan.md)
- [OpenOnco clinical-review privacy/compliance plan](docs/openonco-clinical-review-privacy-compliance-plan.md)

## How TaskTorrent Works

1. A project publishes chunk specs under `chunks/<project>/`.
2. Maintainers open active chunks as GitHub issues.
3. A contributor or agent claims one chunk.
4. Work lands in an isolated sidecar path in the consumer repo.
5. CI and maintainers verify the output.
6. The maintainer merges, rejects, or asks for revision.

The rule is: **one chunk = one contributor = one PR = one reviewable unit of
work**.

## What Is A Chunk?

A Chunk is a complete LLM-assisted task. A good chunk has:

- a stable chunk ID
- a concrete manifest of entities or files
- allowed and disallowed sources
- an output schema or file format
- machine-checkable acceptance criteria
- maintainer-checked semantic criteria
- explicit rejection criteria
- a claim method
- a Drop estimate

Chunks are grouped by folders and GitHub labels, not by heavyweight project
management layers.

## What Is A Drop?

A Drop is an approximate planning measure for AI work capacity. In this repo,
1 Drop means about 100k tokens of structured AI-assisted work.

A Drop is not money, crypto, credit, a reward, or a transferable asset. It is
only a sizing estimate.

## Maintainer Quickstart

You do not need to install anything to start planning. Give your coding agent
this prompt inside your project:

```text
You are helping me adopt TaskTorrent for this repository.

Read https://github.com/romeo111/task_torrent and use its README,
docs/cross-repo-contract.md, docs/chunk-system.md, and chunks/openonco/
examples as the protocol reference.

Do not write production code yet. First, propose a TaskTorrent integration plan:

1. Identify 5-10 useful chunks that are safe for AI-assisted contributors.
2. For each chunk, define mission, manifest, allowed sources, disallowed
   sources, output format, acceptance criteria, rejection criteria, required
   skill, claim method, and Drop estimate.
3. Mark safety boundaries and maintainer-review requirements.
4. Recommend which chunks should open first as GitHub issues.
5. Produce the first chunk spec in TaskTorrent v0.4 format.

Keep every chunk reviewable as one issue, one contributor, one branch, and one
pull request.
```

Optional local tooling:

```bash
pip install -e ".[dev]"
python -m tasktorrent.lint_chunk_spec --all chunks/
```

Commands:

- `tasktorrent-lint <chunk-spec.md>` validates a chunk spec.
- `tasktorrent-init <consumer-name>` scaffolds a basic consumer integration.

## OpenOnco References

- [OpenOnco first case](docs/openonco-first-case.md)
- [OpenOnco pilot workflow](docs/openonco-pilot-workflow.md)
- [OpenOnco chunk shelf](chunks/openonco/)
- [OpenOnco contributor plugin plan](docs/openonco-contributor-plugin-plan.md)
- [OpenOnco clinical-review privacy/compliance plan](docs/openonco-clinical-review-privacy-compliance-plan.md)
- [Safety rules](docs/safety-rules.md)
- [Cross-repo contract](docs/cross-repo-contract.md)
- [Protocol v0.4 design](docs/protocol-v0.4-design.md)

## Repository Boundary

This repository contains the TaskTorrent protocol, docs, OpenOnco chunk specs,
skill specs, GitHub templates, landing data, and optional linter/scaffold
tooling.

It does not contain OpenOnco production data, a hosted service, autonomous merge
logic, or a replacement for maintainer review.
