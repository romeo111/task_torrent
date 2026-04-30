# SETUP

This is a Claude Code plugin for contributing to OpenOnco TaskTorrent
chunks. It does not run a backend, does not require API keys beyond
your own Claude Code session, and does not install anything outside
your local Claude environment.

## What you need

1. **Claude Code** installed (`claude --version`).
2. A local checkout of the **OpenOnco consumer repo** (`romeo111/OpenOnco`)
   if you want to write sidecars and open PRs against it.
3. A local checkout of **TaskTorrent** (`romeo111/task_torrent`) for
   chunk specs and the linter.
4. **Python 3.10+** and `pip install pyyaml` for the local linter.
5. Optional: **GitHub CLI** (`gh`) if you want Claude to inspect
   GitHub issues or prepare PR work for you.

You do not need to install Anthropic API keys, an MCP server, or any
remote service to use this plugin.

## Install the plugin

The plugin lives at `plugins/openonco-contributor/` inside the
`romeo111/task_torrent` repo. Two ways to use it:

### Option A — via marketplace (recommended)

```text
/plugin marketplace add https://github.com/romeo111/task_torrent
/plugin install openonco-contributor@tasktorrent
```

After install, the slash commands `/openonco-contribute` and
`/openonco-review-chunk` become available, along with the bundled
skills.

### Option B — local plugin directory (development / one-off)

If you have the TaskTorrent repo cloned locally:

```bash
claude --plugin-dir /path/to/task_torrent/plugins/openonco-contributor
```

This loads the plugin only for the current session.

## Verify the install

In a Claude Code session:

```text
/plugin list
```

Should show `openonco-contributor` v0.4.0.

```text
/openonco-contribute
```

Should print the contributor walkthrough prompt.

## Update the plugin

The plugin runs on local repo content. To pick up new chunks or
updated skills, `git pull` in your TaskTorrent checkout, then restart
Claude Code (or re-run `/plugin marketplace update`).

## What the plugin does NOT do

- It does not collect telemetry, analytics, or any user data.
- It does not call a plugin-operated server.
- It does not auto-merge PRs or auto-publish anything.
- It does not edit `knowledge_base/hosted/content/` in the consumer
  repo. All writes go to `contributions/<chunk-id>/`.
- It does not provide medical advice or process PHI. See
  [PRIVACY.md](./PRIVACY.md) and the safety boundary in
  [README.md](./README.md).

## PHI / patient data

Do not paste patient records, names, dates of birth, MRNs, scan
files, pathology reports, or any patient-identifying content into
the session. The plugin will refuse to process such input. See
[PRIVACY.md](./PRIVACY.md) for the full policy.

## Troubleshooting

- **Plugin commands not showing up**: run `/plugin list`. If
  `openonco-contributor` is missing, re-run the install step.
- **Skills not activating**: verify your chunk path matches the
  `contributions/<chunk-id>/` convention; the skills key off chunk
  manifest content.
- **Linter complains**: `python -m tasktorrent.lint_chunk_spec
  chunks/openonco/<chunk-id>.md` — fix the chunk spec, do not
  bypass.
- **PR validation fails**: do not use `--no-verify`. Fix the
  underlying issue. See the citation-verification skill for
  verifier-disagreement handling.

## Issues

Report plugin bugs, false refusals, or missing refusals at
https://github.com/romeo111/task_torrent/issues. See
[SECURITY.md](./SECURITY.md) for vulnerability reports.
