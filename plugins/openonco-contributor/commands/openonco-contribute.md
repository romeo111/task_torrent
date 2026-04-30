---
name: openonco-contribute
description: Walk the user through claiming and completing one OpenOnco TaskTorrent chunk end-to-end — pick a claimable chunk, summarize scope, draft sidecars under `contributions/<chunk-id>/`, run validation, prepare one PR, and stop.
user-invocable: true
---

You are helping the user contribute one TaskTorrent chunk to OpenOnco
cancer-research data work.

Use only local files and user-provided context unless the user explicitly
asks you to fetch current GitHub issue state. Pick exactly one currently
claimable OpenOnco chunk. If no chunk is claimable, stop and report that
the shelf is between active waves.

## Required reading before you start

Tell the user you will read these and ask them to point you to local
copies if they are not in the working directory:

- `https://github.com/romeo111/task_torrent` — the protocol repo
- `docs/openonco-pilot-workflow.md` — source allowlist, banned sources, sidecar conventions
- `chunks/openonco/` — current chunk shelf
- `https://github.com/romeo111/OpenOnco` — the consumer repo where sidecars are merged

## Pre-flight summary (always)

Before writing files, summarize back to the user:

1. The chunk ID and (if known) the GitHub issue number.
2. The manifest you will own (concrete entity IDs / filename ranges).
3. Allowed sources and banned sources for this chunk.
4. Output path under `contributions/<chunk-id>/`.
5. Validation commands you will run.

Wait for the user to confirm before starting work.

## Hard rules

- Work only under `contributions/<chunk-id>/` unless the chunk explicitly
  authorizes another path.
- Do not edit `knowledge_base/hosted/content/`.
- Do not write treatment advice, patient-specific recommendations,
  diagnosis, triage, or dosing decisions.
- Do not use OncoKB, SNOMED CT, MedDRA, or any banned source.
- Do not use `git add -A`, `git add .`, or `--no-verify`.
- One chunk = one contributor = one PR. Open one PR, then stop.
- Do not process PHI. If user content includes patient identifiers
  (names, DOB, MRN, scans, pathology reports, case histories), stop and
  ask the user to remove identifiers and reframe the request as evidence
  or provenance review.

## Skill selection

Choose the right plugin skill for the work:

- `citation-verification` — verify (claim, source) pairs, emit citation-report.yaml
- `biomarker-sidecar-draft` — draft BMA-* / BIO-* sidecars
- `drug-evidence-mapping` — draft DRUG-* / IND-* sidecars
- `source-stub-prep` — prepare source_stub.yaml for a new SRC-* candidate
- `chunk-readiness-review` — pre-flight a chunk spec before claiming

If the chunk needs more than one skill, run them in sequence and write
each output to its own file.

## Validation before PR

Before opening the PR, run:

```bash
python -m tasktorrent.lint_chunk_spec chunks/openonco/<chunk-id>.md
python -m pytest tests/test_lint_chunk_spec.py tests/test_openonco_job.py -q
```

If the consumer repo has the citation verifier installed:

```bash
python -m scripts.tasktorrent.verify_citations <chunk-id>
```

Fix any failures before the PR. Do not bypass with `--no-verify`.

## When to stop

Stop after:

- the PR is opened, OR
- a blocking issue is found that needs maintainer input, OR
- the user asks you to stop, OR
- no chunk is currently claimable.

This command is review support only. It is not medical advice and does
not approve hosted clinical content for publication.
