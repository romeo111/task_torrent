# Onboarding a new consumer to TaskTorrent

A "consumer" is any repo that uses TaskTorrent to coordinate distributed AI work — OpenOnco is the first; civic-tech and open-research projects can follow.

This doc covers two steps:

1. **Mandatory + active:** register your repo in `consumers.yaml` so it appears on the [TaskTorrent landing page](https://romeo111.github.io/task_torrent/) and gets included in the 4-hourly metrics build.
2. **Proposal only — DO NOT enable yet** (as of 2026-04-29): a webhook flow that triggers near-real-time landing-page rebuilds. Documented for design review while parallel chunk-execution work stabilizes. **Maintainer will announce in CHANGELOG when this path is open for opt-in.**

Step 1 takes ~5 minutes. Step 2 stays as a planning doc until further notice.

---

## Step 1 — Register your repo

Open a PR to `romeo111/task_torrent` adding an entry to `consumers.yaml`:

```yaml
consumers:
  - name: <short-id>             # lowercase, no spaces, e.g. openonco
    display_name: "<Project Name> — <one-line tagline>"
    repo: <owner>/<repo>         # e.g. romeo111/OpenOnco
    chunks_path: chunks/<short-id>/
    contributions_path: contributions/
    contribute_url: <optional public landing on your site>
    description: >
      2-3 sentences describing the project's purpose, scope, and any
      hard constraints (banned sources, two-reviewer signoff, etc).
    safety_notes:
      - "<one rule per line>"
    webhook_enabled: false       # flip to true after Step 2 completes
```

Maintainer reviews and merges. Within ~4 hours your repo appears on the landing page.

### What the build pulls from your repo

- `gh issue list --label chunk-task --state all` — all chunk-task issues, used to count completed/active/claimable chunks.
- For each `_contribution_meta.yaml` under your `contributions_path/`: optional `cost_actual.tokens` (real token cost) + `contributor` (for unique-contributor count, **not displayed publicly**, only counted).

If your repo doesn't have these conventions yet, the build degrades to "completed: 0, claimable: 0" rather than failing.

---

## Step 2 — Webhook for near-real-time updates (optional)

> ⚠️ **PROPOSAL — DO NOT ENABLE YET (as of 2026-04-29).** The webhook path is documented as a v0.5+ enhancement, not a v0.4 deliverable. While parallel chunk-execution work is in flight in OpenOnco, **do not configure webhooks in any consumer repo** — the cron baseline is intentionally the only active path. The webhook listener in this repo's `build-landing.yml` is dormant: it accepts `repository_dispatch` events but nobody is firing them. Re-enable this section's instructions only after the maintainer announces "webhook flow is open" in CHANGELOG.

Without webhook setup, the landing page updates every 4 hours via cron. With webhook setup, it updates within ~30 seconds of a PR merge or issue close in your repo.

### What you need

- Admin access to your consumer repo (to add a workflow + secret)
- A GitHub Personal Access Token (PAT) with **`repo` scope** that can call repository_dispatch on `romeo111/task_torrent`. See https://github.com/settings/tokens — fine-grained PAT works too if granted "Contents: Read and write" + "Metadata: Read" + "Actions: Read and write" on `romeo111/task_torrent`.

### Setup

**1. Add the PAT as a secret in your repo.**

In your repo: Settings → Secrets and variables → Actions → New repository secret.
- Name: `TASKTORRENT_DISPATCH_TOKEN`
- Value: your PAT

**2. Add the workflow.**

Create `.github/workflows/tasktorrent-dispatch.yml` in your repo:

```yaml
name: Dispatch TaskTorrent landing rebuild

on:
  pull_request:
    types: [closed]
  issues:
    types: [closed, opened, labeled, unlabeled, assigned, unassigned]

permissions:
  contents: read

jobs:
  dispatch:
    # Only fire on events that actually change chunk state
    if: |
      (github.event_name == 'pull_request' && github.event.pull_request.merged == true) ||
      (github.event_name == 'issues' &&
        contains(github.event.issue.labels.*.name, 'chunk-task'))
    runs-on: ubuntu-latest
    steps:
      - name: Fire repository_dispatch on task_torrent
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.TASKTORRENT_DISPATCH_TOKEN }}" \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/repos/romeo111/task_torrent/dispatches" \
            -d '{"event_type": "consumer-update", "client_payload": {"source_repo": "${{ github.repository }}"}}'
```

**3. Update your `consumers.yaml` entry.**

Open a follow-up PR setting `webhook_enabled: true` for your consumer entry.

### Verify

After step 2, do a test issue comment / label change on a chunk-task issue. Within ~30 seconds:

- task_torrent's [Build landing workflow](https://github.com/romeo111/task_torrent/actions/workflows/build-landing.yml) should show a fresh run with reason `repository_dispatch`.
- Your repo's [Dispatch workflow](https://github.com/<your-repo>/actions/workflows/tasktorrent-dispatch.yml) should show a successful run.

If the dispatch fails with 401/403, your PAT is wrong or doesn't have the right scope. Regenerate.

---

## Failure modes + reconciliation

- **Webhook missed:** GitHub webhooks are at-most-once. If a delivery fails (rare but happens), the data is stale until the next cron tick (≤4 hours). The cron is the safety net; webhooks are the optimization.
- **PAT expired:** workflow logs show 401. Regenerate PAT and update the secret.
- **Consumer repo unavailable:** `build_landing_data.py` logs a warning for that consumer and continues with others. Your KPIs show `—` until the repo is reachable again.

## Privacy note

The landing page shows aggregate counts only:
- Total chunks completed across projects
- Estimated tokens transferred
- Number of currently-claimable chunks
- Per-consumer breakdown (counts, no usernames)

Contributor identities (`_contribution.contributor` from sidecar metas) are read for de-duplicated **counting** only and are never emitted to the public JSON or page.

## Removing a consumer

Open a PR removing the entry from `consumers.yaml`. The next build will drop that consumer from the landing page within 4 hours.
