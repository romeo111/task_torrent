# Changelog

All notable changes to the `openonco-contributor` Claude Code plugin
are recorded here.

The plugin's version tracks the TaskTorrent protocol version it
targets. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

(Next changes land here before tagging a release.)

## [0.4.0] — 2026-04-30

Initial public release. Targets TaskTorrent protocol v0.4. Shipped in
`romeo111/task_torrent` PR #31.

### Added

- Plugin manifest at `.claude-plugin/plugin.json` (`name=openonco-contributor`,
  MIT, description carries "Not medical advice").
- Repo-root marketplace listing at `.claude-plugin/marketplace.json`.
- Five bundled skills:
  - `citation-verification` — verify (claim, source) pairs from a
    chunk manifest, emit `citation-report.yaml`.
  - `biomarker-sidecar-draft` — draft `BiomarkerActionability` (BMA-*)
    and `Biomarker` (BIO-*) sidecars from manifest-owned entities.
  - `drug-evidence-mapping` — draft `Drug` (DRUG-*) and `Indication`
    (IND-*) sidecars with two-Clinical-Co-Lead-signoff metadata.
  - `source-stub-prep` — prepare `source_stub_<id>.yaml` for real,
    accessible, allowed sources; refuse banned sources.
  - `chunk-readiness-review` — lint a chunk spec against TaskTorrent
    v0.4 protocol; defers to `tasktorrent/lint_chunk_spec.py`.
- Two user-invocable commands:
  - `/openonco-contribute` — end-to-end contributor walkthrough.
  - `/openonco-review-chunk` — pre-claim chunk readiness review.
- Plugin docs: README, SETUP, EXAMPLES (6 worked scenarios incl.
  refusals + between-wave path), PRIVACY, SECURITY, SUPPORT, LICENSE.

### Safety boundaries baked into descriptions and command preambles

- Refuses treatment advice, hosted-content edits, PHI.
- Refuses banned sources (OncoKB, SNOMED CT, MedDRA) on sight,
  including the social-engineering case where the user claims a
  chunk's Allowed Sources permits OncoKB.
- `chunk-readiness-review` requires running the linter via Bash
  before reporting blocking issues; will not paraphrase the linter.

### Verification

- `claude plugin validate plugins/openonco-contributor` → passes.
- `claude plugin validate .claude-plugin/marketplace.json` → passes.
- Smoke-tested via `claude -p` with Haiku 4.5 across:
  install + enable, slash-command discovery, skill registration under
  `openonco-contributor:*` namespace, treatment-advice refusal,
  banned-source refusal across three skills, pre-flight summary on
  a real chunk spec.

### Migrated

- `skills/citation-verification.md` → `plugins/openonco-contributor/skills/citation-verification/SKILL.md`
- `skills/biomarker-extraction.md` → `plugins/openonco-contributor/skills/biomarker-sidecar-draft/SKILL.md` (renamed)
- `skills/drug-evidence-mapping.md` → `plugins/openonco-contributor/skills/drug-evidence-mapping/SKILL.md`

The original repo-level skill files were removed in the same release;
plugin paths are now canonical.

### Known limitations

- No bundled MCP server. v1 reads local files and user-supplied
  context only.
- No GitHub Actions hooks for `claude plugin validate` on push at v1
  ship-time (added shortly after release).
- One real end-to-end contributor PR against `romeo111/OpenOnco` not
  yet observed at v1 ship-time. See `docs/openonco-plugin-handoff-plan.md`
  Step 5.

[Unreleased]: https://github.com/romeo111/task_torrent/compare/openonco-contributor--v0.4.0...HEAD
[0.4.0]: https://github.com/romeo111/task_torrent/releases/tag/openonco-contributor--v0.4.0
