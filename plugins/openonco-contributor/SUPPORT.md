# SUPPORT

## Where to ask usage questions

- **Plugin behavior, skill activation, command flow** — open an
  issue at https://github.com/romeo111/task_torrent/issues with
  the label `plugin`.
- **OpenOnco protocol questions** (chunk shape, source policy,
  sidecar conventions) — same repo, label `protocol`.
- **OpenOnco knowledge content** (specific BMA / Drug / Indication
  data, clinical correctness) — these belong to the consumer repo,
  https://github.com/romeo111/OpenOnco. Open issues there.

## Report a bug or unexpected refusal

Open a regular issue with:

- Plugin version (`/plugin list` output)
- Claude Code version
- OS
- The exact prompt you ran
- What you expected
- What happened
- A minimal reproduction if possible

Common bug categories the maintainer cares about:

- **False refusal** — the plugin refused safe contributor work
  (e.g. citation verification on a clearly allowed source).
- **Missing refusal** — the plugin processed input it should have
  refused (treatment advice, PHI, banned sources, hosted-content
  edits).
- **Schema drift** — sidecar output no longer matches the
  consumer-repo schema.
- **Chunk drift** — `chunk-readiness-review` disagrees with
  `tasktorrent/lint_chunk_spec.py`.

For false / missing refusals, label the issue `safety` so the
maintainer triages it sooner.

## Expected response model

This is a community-maintained plugin. There is no SLA. Maintainers
aim to triage issues within a week, but no response time is
guaranteed.

For urgent safety-relevant reports, see [SECURITY.md](./SECURITY.md).

## What support does not cover

- **Medical advice.** This plugin does not provide medical advice
  and support cannot answer "what should I prescribe" or
  "what is the best treatment for X" questions. Those belong with
  a treating clinician.
- **Patient-specific care.** Do not include PHI in support
  requests. PHI in issues will be redacted and the report
  triaged separately.
- **Anthropic Claude itself.** Bugs in the underlying Claude
  model belong with Anthropic. Plugin issues belong here.
- **Consumer-repo content correctness.** Disputes about whether
  a specific BMA, Drug, or Indication is correct go to the
  OpenOnco repo, not this plugin's issue tracker.
- **Direct PR support.** Reviewers in the consumer repo (OpenOnco
  maintainers and Clinical Co-Leads) own the merge decision. This
  plugin produces drafts; it does not have a fast path to merge.

## Reading order if you're stuck

1. [README.md](./README.md) — what the plugin is and isn't.
2. [SETUP.md](./SETUP.md) — install + verify steps.
3. [EXAMPLES.md](./EXAMPLES.md) — six worked scenarios including
   refusals.
4. [PRIVACY.md](./PRIVACY.md) — PHI policy and data handling.
5. [SECURITY.md](./SECURITY.md) — vulnerability reporting.
6. `docs/openonco-pilot-workflow.md` in the TaskTorrent repo —
   source allowlist and sidecar conventions.
