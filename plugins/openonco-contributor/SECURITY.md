# SECURITY

## Reporting a vulnerability

Open a private security advisory at
https://github.com/romeo111/task_torrent/security/advisories/new
or, if that is not available, file a regular issue at
https://github.com/romeo111/task_torrent/issues with the title
prefix `[SECURITY]` and minimal detail; a maintainer will reach
out to coordinate.

When you file a report:

- **Do not** include patient health information (PHI), secrets,
  tokens, API keys, credentials, or private patient data.
- **Do** include: plugin version (`/plugin list`), Claude Code
  version, OS, reproduction steps, expected vs. observed
  behavior, and any safety relevance (e.g. refusal that should
  have fired but didn't).

## Supported versions

Currently supported: `openonco-contributor` v0.4.x.

Older 0.x versions are not supported. Always use the version
matching the TaskTorrent protocol release noted in the plugin's
README and the consumer-repo CHARTER.

## What the plugin does and does not have

- **No API keys** beyond what you already manage in Claude Code.
- **No remote MCP server** in v1.
- **No plugin-operated backend** in v1.
- **No auto-merge** capability — the plugin cannot merge PRs.
- **No direct publication** — the plugin cannot edit
  `knowledge_base/hosted/content/`.
- **No installer script** — the plugin does not run shell
  bootstraps. Setup is via `/plugin install` or `--plugin-dir`.

## Threat model

Things this plugin tries to defend against:

| Threat | Mitigation |
|---|---|
| User asks for treatment advice | Refusal in every skill + commands |
| User pastes PHI | PHI gate refusal in every skill |
| Banned source proposed | `source-stub-prep` refuses OncoKB / SNOMED CT / MedDRA |
| Hosted content edit attempted | Skills restrict output to `contributions/<chunk-id>/` |
| Recommendation wording in drafts | Drafting skills require neutral wording, no "best/first-line" language |
| Bypass via `--no-verify` | Commands explicitly forbid bypass |
| Chunk drift from protocol | `chunk-readiness-review` defers to `tasktorrent/lint_chunk_spec.py` |

## What this plugin does not defend against

- Adversarial users who copy-paste plugin output and apply it to
  patient care anyway. The plugin's outputs are review drafts;
  clinical decisions remain with maintainers, clinical leads, and
  ultimately treating clinicians.
- Compromised local environments, malicious MCP servers, or
  malicious GitHub state that the user has authenticated.
- Plugin dependency tampering — v1 has no dependencies, so this
  is currently moot. Future dependency-bearing versions will pin
  semver ranges and re-run unsafe-prompt tests before widening.

## Coordinated disclosure

We aim to acknowledge security reports within 5 business days and
to confirm fix timelines within 15 business days for confirmed
issues. Where appropriate, we will credit the reporter in the
release notes.
