# OpenOnco TaskTorrent Contributor

A Claude Code plugin for donating AI-agent time to
[OpenOnco](https://github.com/romeo111/OpenOnco), a free oncology
clinical decision-support knowledge base, by completing one
reviewable [TaskTorrent](https://github.com/romeo111/task_torrent)
chunk at a time.

> **Not medical advice.** This plugin produces sidecar drafts,
> citation reports, source stubs, and review checklists for
> OpenOnco maintainers. It does not provide medical advice, does
> not edit hosted clinical content, does not auto-merge or auto-publish,
> and does not process PHI.

## What's in the plugin

| Component | What it does |
|---|---|
| `/openonco-contribute` | End-to-end walkthrough: pick a chunk, summarize scope, draft sidecars, validate, prepare one PR, stop. |
| `/openonco-review-chunk` | Pre-claim readiness review of a TaskTorrent v0.4 chunk spec. Reports blocking issues, warnings, source-policy notes. |
| Skill: `citation-verification` | Verify (claim, source) pairs from a chunk manifest; emit `citation-report.yaml`. |
| Skill: `biomarker-sidecar-draft` | Draft `BiomarkerActionability` (BMA-*) and `Biomarker` (BIO-*) sidecars from manifest-owned entities. |
| Skill: `drug-evidence-mapping` | Draft `Drug` (DRUG-*) and `Indication` (IND-*) sidecars with two-Clinical-Co-Lead-signoff metadata. |
| Skill: `source-stub-prep` | Prepare `source_stub_<id>.yaml` for a real, accessible, allowed source. Refuses banned sources. |
| Skill: `chunk-readiness-review` | Lint a chunk spec against TaskTorrent v0.4 protocol; defers to `tasktorrent/lint_chunk_spec.py`. |

## Safety boundary

Every skill and command enforces:

1. Work on exactly one chunk.
2. Stay inside `contributions/<chunk-id>/` unless the chunk explicitly
   permits another path.
3. Drafts only — maintainers review every output before merge.
4. Do not edit `knowledge_base/hosted/content/`.
5. Do not write treatment advice or patient-specific output.
6. Do not use OncoKB, SNOMED CT, MedDRA, or any banned source.
7. Do not process PHI.
8. Do not bypass validation. No `git add -A`, no `git add .`, no
   `--no-verify`.
9. One chunk = one contributor = one PR.

## Install

See [SETUP.md](./SETUP.md). Short version:

```text
/plugin marketplace add https://github.com/romeo111/task_torrent
/plugin install openonco-contributor@tasktorrent
```

## Use

```text
/openonco-contribute
```

The command picks one currently claimable chunk, summarizes the
scope, asks you to confirm, runs the right plugin skill, writes
sidecars under `contributions/<chunk-id>/`, runs validation, and
stops after one PR.

If no chunk is claimable, the command says so and stops — see
[EXAMPLES.md](./EXAMPLES.md) Example 6.

## Documentation

- [SETUP.md](./SETUP.md) — install, verify, troubleshoot.
- [EXAMPLES.md](./EXAMPLES.md) — six worked scenarios (3 safe + 2
  unsafe-refusal + 1 between-wave).
- [PRIVACY.md](./PRIVACY.md) — PHI policy, data handling, what the
  plugin does not collect.
- [SECURITY.md](./SECURITY.md) — vulnerability reporting, threat
  model.
- [SUPPORT.md](./SUPPORT.md) — where to ask, what is and isn't
  supported.
- [LICENSE](./LICENSE) — MIT.

## What this plugin is not

- It is not a medical device, decision-support system, or clinical
  recommendation engine.
- It is not a marketplace, payment system, token system, or hosted
  bot.
- It is not a replacement for OpenOnco maintainer review or
  Clinical Co-Lead signoff.
- It is not a way to publish hosted clinical content directly.

## Versioning

Initial release `0.4.0`, matching the TaskTorrent v0.4 protocol the
plugin targets. Bumps follow the protocol: `0.5.0` when v0.5 ships,
`1.0.0` only after public listing and at least one wave of observed
contributor use.

## Source

- Plugin source: `plugins/openonco-contributor/` in
  https://github.com/romeo111/task_torrent
- TaskTorrent protocol: same repo, `docs/` and `tasktorrent/`.
- OpenOnco consumer repo: https://github.com/romeo111/OpenOnco
