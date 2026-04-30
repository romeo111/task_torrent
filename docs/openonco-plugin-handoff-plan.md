# OpenOnco Plugin Handoff Plan

## Status

Hand-off plan for the `openonco-contributor` Claude Code plugin (v0.4.0,
shipped on branch `codex/plugin-dependency-plan`, [PR #31](https://github.com/romeo111/task_torrent/pull/31)).

Goal: get the plugin into the hands of OpenOnco contributors and
maintainers so it can be used on the two currently-active chunks
([#11](https://github.com/romeo111/task_torrent/issues/11),
[#12](https://github.com/romeo111/task_torrent/issues/12)), then submitted
to the Anthropic plugin directory for public listing.

## Current state

- Plugin source: `plugins/openonco-contributor/` in `romeo111/task_torrent`.
- Marketplace: `.claude-plugin/marketplace.json` at repo root.
- Validation: `claude plugin validate plugins/openonco-contributor` ✓.
- 5 skills, 2 commands, 7 docs (README/SETUP/EXAMPLES/PRIVACY/SECURITY/SUPPORT/LICENSE).
- LICENSE: MIT, both at repo root and inside the plugin.
- Smoke-tested via `claude -p` (Haiku 4.5):
  - Plugin install + enable: ✓
  - `/openonco-contribute` and `/openonco-review-chunk` registered: ✓
  - 5 skills under `openonco-contributor:*` namespace: ✓
  - Treatment-advice refusal: ✓
  - OncoKB / SNOMED CT / MedDRA refusal across 3 skills: ✓ (after fix `9fda377`)
  - Pre-flight summary on a real chunk spec: ✓

## Active chunks (currently claimable)

| Issue | Chunk ID | Type | Drops |
|---|---|---|---:|
| [task_torrent#11](https://github.com/romeo111/task_torrent/issues/11) | `civic-bma-reconstruct-all` | BMA reconstruction (399 BMAs from CIViC snapshot) | ~12 |
| [task_torrent#12](https://github.com/romeo111/task_torrent/issues/12) | `citation-verify-914-audit` | Citation verification (914 findings) | ~10 |

Both have `status-active`, `pilot-active`, `chunk-task` labels and no
assignees as of 2026-05-01.

## Architectural mismatch — fix before broad announcement

`consumers.yaml` declares OpenOnco's chunk repo as `romeo111/OpenOnco`,
but the actual `[Chunk]` issues are filed in `romeo111/task_torrent`
itself. As a result:

- `scripts/build_landing_data.py` queries `romeo111/OpenOnco/issues?labels=chunk-task` and finds zero.
- Landing page metrics show `claimable=0` even though 2 chunks are active.
- `landing/metrics.json` and `landing/chunks.json` do not surface the
  active chunks.

Two ways to resolve, listed in increasing scope of change:

**Option A — change the builder (minimal)**

Add a `chunk_issues_repo` field to consumers.yaml that defaults to the
consumer repo but can be overridden. Set `chunk_issues_repo: romeo111/task_torrent`
for OpenOnco. Update `fetch_consumer_stats()` to query that repo for
issues. The chunk specs continue to live in task_torrent, the chunk
issues continue to live in task_torrent, and contributors still PR into
the consumer repo (`romeo111/OpenOnco`).

**Option B — move chunk issues to OpenOnco (canonical)**

Open mirror issues #N and #N+1 in `romeo111/OpenOnco` with the same
chunk specs, close the originals in task_torrent with a "moved to" link.
Going forward, all chunk issues open in the consumer repo. This matches
the README's "the consumer opens active chunks as GitHub issues"
narrative and makes the builder Just Work.

**Recommendation**: do Option A in this PR (or a follow-up) so the
landing page is correct now; consider Option B as a separate
maintainer-coordination project.

## Stale paths in active issue bodies

Issue #11 references `skills/biomarker-extraction.md` and issue #12
references `skills/citation-verification.md`. Both paths were migrated
into the plugin in commit `1864cfd`:

| Old path | New path |
|---|---|
| `skills/biomarker-extraction.md` | `plugins/openonco-contributor/skills/biomarker-sidecar-draft/SKILL.md` |
| `skills/citation-verification.md` | `plugins/openonco-contributor/skills/citation-verification/SKILL.md` |
| `skills/drug-evidence-mapping.md` | `plugins/openonco-contributor/skills/drug-evidence-mapping/SKILL.md` |

A contributor opening these issues today and clicking through the
"Required Skill" link will get a 404. Two options:

- **Edit the issue bodies** to update paths (issue body is mutable; this
  is the cleanest fix).
- **Comment on the issues** with the migration note and a pointer at
  `/plugin install openonco-contributor@tasktorrent` (less invasive but
  contributors must scroll to find the comment).

Recommendation: edit the issue bodies (one-line path swap), then add a
comment announcing the plugin and giving the install steps.

## Handoff steps (ordered)

### Step 1 — Land PR #31 in task_torrent (this PR)

- [x] Plugin shipped, validated, smoke-tested.
- [x] Plans finalized.
- [ ] Merge into `main`.

### Step 2 — Fix landing-page metrics

Pick Option A above (or B). Re-run `python scripts/build_landing_data.py`.
Confirm `landing/metrics.json` shows `chunks_claimable: 2` and
`landing/chunks.json` lists both active chunks.

### Step 3 — Patch active issue bodies

Edit `[Chunk] OpenOnco civic-bma-reconstruct-all` ([#11](https://github.com/romeo111/task_torrent/issues/11)):

- Change `Required Skill: skills/biomarker-extraction.md` to
  `plugins/openonco-contributor/skills/biomarker-sidecar-draft/SKILL.md`.

Edit `[Chunk] OpenOnco citation-verify-914-audit` ([#12](https://github.com/romeo111/task_torrent/issues/12)):

- Change `Required Skill: skills/citation-verification.md` to
  `plugins/openonco-contributor/skills/citation-verification/SKILL.md`.

Add an identical comment to both:

```markdown
**Plugin available**: this chunk is now supported by the
`openonco-contributor` Claude Code plugin (v0.4.0). Install:

    /plugin marketplace add https://github.com/romeo111/task_torrent
    /plugin install openonco-contributor@tasktorrent

Then run `/openonco-contribute` to walk the workflow end-to-end. The
plugin's skill bundle covers citation-verification, biomarker-sidecar-draft,
drug-evidence-mapping, source-stub-prep, and chunk-readiness-review.

The original `skills/<name>.md` paths have been migrated into the plugin
at `plugins/openonco-contributor/skills/<name>/SKILL.md`. Other coding
agents (Codex, Cursor, ChatGPT) should reference the plugin path
directly. See [`README.md` "Contribute To Cancer Research"](https://github.com/romeo111/task_torrent#contribute-to-cancer-research)
for both paths.
```

### Step 4 — Coordinate with OpenOnco maintainer

Open an issue or PR in `romeo111/OpenOnco`:

- Update `OpenOnco/contribute.html` (the consumer-facing contribution
  guide referenced in `consumers.yaml`'s `contribute_url`) to mention
  the plugin install path alongside the existing prompt-block path.
- Confirm with the maintainer that the architecture (Option A vs B
  above) is acceptable.
- Announce in any project channel (Discord/Slack/Telegram if any) that
  the plugin is live for the two active chunks.

### Step 5 — One real end-to-end run before public listing

This is the smoke test we cannot do from this session: a contributor
or the maintainer should:

1. Clone `romeo111/OpenOnco` locally.
2. Install the plugin: `/plugin install openonco-contributor@tasktorrent`.
3. Run `/openonco-contribute`, claim issue #11 or #12.
4. Let the plugin draft sidecars under `contributions/<chunk-id>/`.
5. Run `python -m tasktorrent.lint_chunk_spec <path>` and the citation
   verifier (when applicable) before opening the PR.
6. Open one PR, then stop.
7. Report any false refusals, missing refusals, or schema drift to
   `task_torrent/issues`.

### Step 6 — Submit to the Anthropic plugin directory

Once Step 5 is complete and any rough edges are fixed:

1. Confirm `claude plugin validate plugins/openonco-contributor` passes.
2. Tag the release: `claude plugin tag plugins/openonco-contributor --push`
   should produce `openonco-contributor--v0.4.0`.
3. Submit the plugin via the Anthropic plugin directory submission flow.
   The submission needs:
   - Public GitHub repo URL
   - Plugin description with "Not medical advice" already in
     [`plugin.json`](../plugins/openonco-contributor/.claude-plugin/plugin.json)
   - Privacy policy: [`PRIVACY.md`](../plugins/openonco-contributor/PRIVACY.md)
   - Security contact: [`SECURITY.md`](../plugins/openonco-contributor/SECURITY.md)
   - Support contact: [`SUPPORT.md`](../plugins/openonco-contributor/SUPPORT.md)
   - 6 worked examples: [`EXAMPLES.md`](../plugins/openonco-contributor/EXAMPLES.md)

### Step 7 — Plan the clinical-review plugin

After contributor plugin is stable AND OpenOnco maintainers approve the
no-PHI boundary: build `openonco-clinical-review` per
[the existing plan](openonco-clinical-review-privacy-compliance-plan.md).
Different repo branch, different PR. Do not bundle.

## Risks at handoff

| Risk | Severity | Mitigation |
|---|---:|---|
| Contributor follows stale skill path in issue body | Medium | Step 3 — edit issue bodies and comment |
| Landing metrics keep showing 0 | Medium | Step 2 — fix builder or move chunks |
| OpenOnco maintainer wants different plugin scope | Low | Step 4 — coordinate before broad announcement |
| Anthropic directory rejects on PHI / medical-advice grounds | Low | `description` carries "Not medical advice"; refusals are smoke-tested; clinical-review intentionally deferred |
| Real end-to-end discovers schema drift | Medium | Step 5 catches it locally before public listing |
| Plugin marketplace `source: ./plugins/openonco-contributor` breaks for non-task_torrent installers | Low | Tested with `claude plugin install openonco-contributor@tasktorrent` from local marketplace |

## Done when

- [ ] PR #31 merged.
- [ ] Landing metrics show `chunks_claimable: 2` (or whatever is true).
- [ ] Issue #11 and #12 bodies updated; comment posted on both.
- [ ] At least one contributor-or-maintainer ran the full flow on one of
      the active chunks and reports the plugin worked end-to-end.
- [ ] `claude plugin tag --push` produces a valid release tag.
- [ ] Submission filed in the Anthropic plugin directory.
- [ ] Anthropic listing confirmed (or feedback received and addressed).
