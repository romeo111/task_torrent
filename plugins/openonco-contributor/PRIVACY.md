# PRIVACY

## What this plugin does with data

This plugin runs entirely inside your Claude Code session. It does
not operate a backend, does not run an MCP server, and does not call
any plugin-operated network endpoint. It works on:

- local repository files in your TaskTorrent / OpenOnco checkout
- content you paste into the Claude Code session
- GitHub state you explicitly ask Claude to fetch (via `gh` or
  user-supplied URLs)

There is no plugin-owned data store, no plugin-owned analytics, and
no plugin-owned telemetry.

## Allowed data

- TaskTorrent protocol docs (public)
- OpenOnco chunk specs and contributor sidecars (public)
- Allowed-list public sources (CIViC, PubMed Central OA, DailyMed,
  openFDA, ClinicalTrials.gov, ESMO/ASCO open guidelines, NCCN
  guidelines by reference, WHO Classification by reference, МОЗ
  України orders)
- Maintainer review notes and contributor metadata

## Prohibited data — PHI

This plugin must not be used to process patient health information
(PHI). Do not paste any of the following into the session:

- Patient names, initials, or pseudonyms
- Dates of birth, encounter dates tied to identity, ages combined
  with disease + treatment context
- Medical record numbers (MRN), patient IDs, hospital accession
  numbers
- Addresses, phone numbers, email addresses, postcodes
- Medical scans, pathology reports, imaging files, lab reports
  with patient identifiers
- Patient case histories, clinical notes, chart summaries
- Genomic test reports tied to an identified patient
- Insurance, payer, or claims data tied to identity

If your input includes any of the above, the plugin will stop and
ask you to remove the identifiers and reframe the request as
evidence or provenance review.

## Refusal language (built into every skill)

```text
I can't process patient-identifying or patient-specific clinical
information. Please remove identifiers and reframe the request as
evidence provenance, citation support, or sidecar review. I can
help review whether a public source supports an OpenOnco claim,
but I can't recommend treatment for a patient.
```

## What the plugin does not do

- It does not collect, store, or transmit data to any
  plugin-operated server.
- It does not retain conversation content beyond your local Claude
  Code session state.
- It does not contact any external service except through tools
  you have already authorized in your Claude Code environment
  (e.g. `gh`, `git`, your own MCP servers).
- It does not export review content automatically.
- It does not auto-merge PRs or auto-publish hosted clinical content.

## GitHub interactions

When the plugin uses `gh` or `git` to inspect chunk issues, prepare
PRs, or pull repo state, those actions:

- happen only when you ask
- use your authenticated GitHub identity
- are visible in your Claude Code transcript
- are subject to your repo permissions

## Data retention

The plugin itself retains nothing. Anthropic's data handling for
your Claude Code session is governed by your Claude Code agreement,
not by this plugin.

## Reporting privacy concerns

Open an issue at
https://github.com/romeo111/task_torrent/issues with the label
`privacy`. Do not include PHI, secrets, or tokens in the issue.
See [SECURITY.md](./SECURITY.md) for vulnerability reports.
