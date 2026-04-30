# Prompt: Update OpenOnco contribute.html for the new plugin

Hand this to a coding agent (Claude Code, Codex, Cursor, etc.) running
inside a local checkout of `romeo111/OpenOnco` to update the public
contributor landing page.

**Target page**: https://openonco.info/contribute.html

**Source**: typically `docs/contribute.html` (or wherever the static
file is built from in `romeo111/OpenOnco`; verify in the repo).

---

## Prompt to paste

```text
You are updating the OpenOnco public contributor landing page to
announce the openonco-contributor Claude Code plugin and to reflect
the two currently-active TaskTorrent chunks.

Background — read first if any of this is unfamiliar:

- TaskTorrent protocol: https://github.com/romeo111/task_torrent
- TaskTorrent README "Contribute To Cancer Research" section:
  https://github.com/romeo111/task_torrent#contribute-to-cancer-research
- The plugin source:
  https://github.com/romeo111/task_torrent/tree/main/plugins/openonco-contributor
- Plugin README:
  https://github.com/romeo111/task_torrent/blob/main/plugins/openonco-contributor/README.md
- Plugin EXAMPLES (worked scenarios incl. refusals):
  https://github.com/romeo111/task_torrent/blob/main/plugins/openonco-contributor/EXAMPLES.md
- Plugin PRIVACY (PHI policy):
  https://github.com/romeo111/task_torrent/blob/main/plugins/openonco-contributor/PRIVACY.md
- Plugin SETUP (install steps):
  https://github.com/romeo111/task_torrent/blob/main/plugins/openonco-contributor/SETUP.md
- Active chunk issues:
    https://github.com/romeo111/task_torrent/issues/11 (BMA reconstruction)
    https://github.com/romeo111/task_torrent/issues/12 (citation verification)

What the page should now communicate:

1. There is a Claude Code plugin called `openonco-contributor` that
   makes the TaskTorrent contribution flow a single command. Install:

       /plugin marketplace add https://github.com/romeo111/task_torrent
       /plugin install openonco-contributor@tasktorrent

   Then run `/openonco-contribute` to walk the flow end-to-end.

2. For contributors using non-Claude agents (Codex, Cursor, ChatGPT,
   etc.), keep the existing prompt-block path. Link to the README
   "Contribute To Cancer Research" section above instead of pasting
   the prompt verbatim, so the page does not drift when the prompt
   updates.

3. Two chunks are currently claimable:
   - civic-bma-reconstruct-all (~12 Drops, mechanical+judgment, BMA
     evidence reconstruction)
   - citation-verify-914-audit (~10 Drops, semantic-NLU, 914-finding
     citation audit)
   Link directly to the GitHub issues above.

4. Make the hard-boundary language clearly visible above the fold,
   not buried in a footer. The page is contributor-facing for a
   clinical-data project, and those rules are the reason the plugin
   is publishable in the Anthropic plugin directory:
   - This is not medical advice.
   - The plugin does not edit hosted clinical content.
   - The plugin does not process PHI. Do not paste patient records,
     names, dates of birth, MRNs, scans, pathology reports, case
     histories, or any identifying clinical information.
   - Banned sources for contributor work: OncoKB, SNOMED CT, MedDRA.

5. Keep the existing wave / metrics / "between waves" language if it
   exists. Do not delete the prompt-block fallback for non-Claude
   agents — keep it as a secondary install path, not the primary.

Concrete edits:

- Add a "Use the Claude Code plugin" section near the top of the page,
  with the two-line install snippet and a single sentence explaining
  what `/openonco-contribute` does.
- Add a "Currently active chunks" section listing the two active
  issues with one-line descriptions.
- Move the existing prompt-block ("You are helping me contribute one
  TaskTorrent chunk...") into a "For other coding agents (Codex,
  Cursor, ChatGPT)" section below the plugin section, with a link to
  the canonical version in the TaskTorrent README rather than an
  inline copy.
- Add or expand a "What this is not" section listing the four hard
  boundaries above (medical advice, hosted-content edits, PHI, banned
  sources).
- Update any "Claimable: 0" or "between waves" copy if the page
  currently says that, since two chunks are now live.

Things you must not do:

- Do not paste medical advice or treatment recommendations on the
  page.
- Do not include patient data examples, even fictitious ones with
  names that look real.
- Do not weaken the no-PHI / no-medical-advice language.
- Do not promise auto-merge, automatic publication, or any path that
  bypasses maintainer review.
- Do not advertise OncoKB / SNOMED CT / MedDRA as usable sources.
- Do not link the plugin to "diagnosis assistant", "treatment
  decision support", or any clinical-decision framing. The plugin is
  a data-curation tool for sidecar drafts; clinical use lives in a
  separate, unshipped plugin track (openonco-clinical-review).

When you are done:

1. Build the page locally if there is a build step (e.g. Jekyll, MkDocs).
2. Open the built HTML in a browser and verify links resolve.
3. Open one PR titled "docs(contribute): announce openonco-contributor
   Claude Code plugin + active chunks" against the OpenOnco repo.
4. In the PR description, link to:
   - https://github.com/romeo111/task_torrent/pull/31
   - https://github.com/romeo111/task_torrent/blob/main/docs/openonco-plugin-handoff-plan.md
5. Stop. Do not merge the PR yourself; await maintainer review.
```

---

## How to use this

Option A — paste the prompt above into Claude Code / Codex / Cursor
inside a `romeo111/OpenOnco` checkout, and let the agent apply edits
plus open the PR.

Option B — hand the prompt to the OpenOnco maintainer in
chat / DM / Slack as a single self-contained instruction so they
can run it through their preferred agent.

Either way, the prompt is designed to stand alone: the agent does not
need this conversation's context, only access to the repo and the
links inside the prompt.
