# Letter to TaskTorrent Owner — 3 Asks From OpenOnco Pilot

**To:** TaskTorrent project owner
**From:** OpenOnco maintainer (post-pilot retrospective)
**Date:** 2026-04-28
**Reading time:** 3 minutes

## Context

OpenOnco ran TaskTorrent's first real-world pilot over 2026-04-27 → 28. Codex contributor agent executed 7 chunks (~70 Drops, ~4M tokens). Result:

- **4 of 7 chunks: net-positive value** (citation triage, rec-wording audit, UA translation review, source-stub ingest)
- **1 of 7: net-negative** (`civic-bma-reconstruct-all`) — should have been a script; this PR's existence cost ~20 Co-Lead-hours pending
- **2 of 7: marginal** — depend on Co-Lead accept-rate, not yet measured
- **4 maintainer-fix PRs** during the wave (validator gaps Codex surfaced)
- **0 of 7 chunks fully applied** to hosted clinical content yet (deferred liability)

Detailed retrospective: `docs/improvements-from-openonco-pilot.md` (12 proposals, PR #15).

## The 3 things to fix this week

If you only do three things, do these. They block the next round of contributor work and they keep TaskTorrent honest.

### 1. Make Economic Profile a required chunk-spec field — TaskTorrent-wide

**Problem:** the chunk-system spec doesn't currently force authors to justify why the chunk earns its keep. OpenOnco pilot's worst chunk (`civic-bma-reconstruct-all`) shipped with a confident "12 Drops, civic-evidence" label that hid the fact that 95% of the work was a script call (`reconstruct_bma_evidence_via_civic.py` already in the repo). Token "savings" evaporated under verification cost.

**Fix:** add Economic Profile as required schema in `docs/chunk-system.md`. PR #14 in this repo already lands this for OpenOnco. Promote to generic.

```yaml
compute_profile: mechanical | llm-essential | mixed
script_alternative: { exists, path, rationale }
verification_cost: { maintainer_hours, expert_hours, expert_specialty }
break_even_test: PASS | MARGINAL | FAIL
```

**Decision rule:** `break_even_test: FAIL` chunks do NOT open. They become script work.

**Why this week:** every additional pilot day without this gate risks repeating the BMA-reconstruct mistake on different work surface (e.g. drug normalization, redflag normalization). Each repeat costs hours that could go to actually-LLM-essential work.

### 2. Ship the validator with permissive-by-default vocabulary

**Problem:** OpenOnco's strict validator forced 4 separate maintainer-fix PRs during the pilot wave (cancer-autoresearch PRs #16, #18, #19, #20). Each was a real bug — validator rejected legitimate Codex output:

- `target_action: review_existing_hosted_draft` — invented but valid semantic; validator rejected as not in `{upsert, new, flag_duplicate}`.
- `task_manifest.txt` rows in `id::path::filename` triple format — validator treated whole line as opaque ID.
- `target_entity_id` missing on `review_existing_*` actions — validator required it; payload's top-level `id` should fall back.
- Banned-source check unconditional — `SRC-ONCOKB` legacy preserved in `review_existing_*` snapshots correctly tripped a check that should only fire for `write` actions.

Each surfaced as a contributor-blocked → maintainer-rushes-fix-PR cycle. That's 4 round-trips per first wave.

**Fix:** ship the reference validator with `extensible-by-config` defaults:

- `TARGET_ACTIONS` = `{write: {upsert, new}, review: {flag_duplicate, review_existing_*}}` — projects extend via config, not hardcode
- `MANIFEST_FORMAT` = parse `id::path::filename` triples, take first field
- `BANNED_SOURCE_CHECK` = hard for write actions, soft for review actions
- `target_entity_id` falls back to top-level `id` for review actions

**Why this week:** every project running TaskTorrent will hit similar validator gaps within hours of first contributor batch. Shipping permissive-by-default saves them the same 4 PRs we ate. Detailed proposals in PR #15 §1, §2, §6 of `improvements-from-openonco-pilot.md`.

### 3. Track value-realized (`applied`) separately from value-merged

**Problem:** OpenOnco pilot has 7 contribution PRs merged to `master`. Sounds like progress. Reality: `0 of 7` actually applied to hosted clinical content. Sidecars sit in `contributions/`. The two audit chunks (rec-wording, ua-translation) produced 2700+ findings sitting as backlog. The 5 entity-write chunks have 500+ sidecars pending Co-Lead signoff.

Current TaskTorrent docs don't distinguish "merged" from "applied". A dashboard showing "7 merged" looks like victory; it actually shows a 2700-finding triage queue + 500-sidecar Co-Lead queue accumulating without progress.

**Fix:** chunk_status becomes two-axis:

```yaml
chunk_status:
  contribution_status: queued | active | merged | rejected
  application_status:  pending | applied | dropped
```

A chunk is "complete" only when `applied`. Shelf views must show both axes. Audit chunks declare a `triage_rate_committed`; if maintainer falls behind, system flags it as "shipped but unrealized".

**Why this week:** without this distinction, projects accumulate backlogs that look like progress. Three weeks of pilots without value realized = pilot is a failure even if every chunk merged. This is the discipline that keeps TaskTorrent from being a vanity-metric machine.

## What I am NOT asking for

- A rewrite of TaskTorrent. The chunk model is correct; the gaps are in governance (Economic Profile), validator defaults, and value-tracking discipline.
- Active development on the dashboard. Phase 4 stuff (capacity matching, contributor profiles, demand queues) doesn't fix the above 3.
- TaskTorrent owner's time on OpenOnco-specific issues. The 3 asks above are project-agnostic; OpenOnco's specifics live in `docs/openonco-pilot-workflow.md`.

## Source data

- `docs/improvements-from-openonco-pilot.md` — full 12 proposals (PR #15)
- `chunks/openonco/*.md` — 7 chunk specs with retroactive Economic Profile fills (PR #14)
- `chunks/openonco/citation-semantic-verify-v2.md` — example of "v2 chunk to deliver v1's disclaimed scope" (PR #16)
- cancer-autoresearch PRs #14, #15, #17, #21 (contributions) and #16, #18, #19, #20 (validator fixes)

## Direct asks (TL;DR)

1. **Ship Economic Profile in `chunk-system.md`** as required — within 1 week.
2. **Ship permissive-by-default validator** — within 1 week.
3. **Add `application_status` axis to chunk_status** — within 2 weeks.

If you do these three, the next pilot project loses 90% of the friction OpenOnco hit. If you don't, every new pilot will eat the same 4 maintainer-fix PRs and accumulate the same invisible backlog.

Happy to discuss tradeoffs / scope-down / push-back on any of the three. The proposals in #15 stand as the longer menu — these three are the gate.

— OpenOnco maintainer
