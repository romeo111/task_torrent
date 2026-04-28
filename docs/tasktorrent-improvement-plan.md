# TaskTorrent Improvement Plan — Living Document

**Status:** living — updated with each new lesson from chunk/torrent runs.
**Source:** OpenOnco pilot (2026-04-27 onward), plus future projects.
**Audience:** TaskTorrent project owner + maintainers.
**Companion docs (frozen snapshots):** `improvements-from-openonco-pilot.md`, `owner-request-from-openonco-pilot.md`. Those were the initial 12-proposal retrospective + 3-ask letter; this document is the consolidated, evolving plan.

This is THE place to look if you want to know "what should TaskTorrent fix, in what order, based on real-world evidence." Each section below is updated as new lessons land.

---

## Top 3 asks (executive summary)

If you only do three things:

1. **Make Economic Profile a required chunk-spec field — TaskTorrent-wide.**
   Prevents repeating the BMA-reconstruct net-negative chunk pattern. Lesson L-1.
2. **Ship the validator with permissive-by-default vocabulary.**
   First-batch contributors hit artificial limits — OpenOnco took 4 fix-PRs in one wave (#16, #18, #19, #20). Lessons L-2, L-13, L-17.
3. **Track value-realized (`applied`) separately from value-merged.**
   7 chunks merged ≠ 7 chunks delivered. Without this distinction, projects accumulate invisible backlogs. Lesson L-9.

Detail in the Asks below; lessons-evidence in §"Lessons learned"; full proposal-tier list in §"Proposed system changes".

---

## Lessons learned (chronological)

Each lesson is one observed pattern + the proposal it drives.

### L-1 — chunk-as-script-substitute (BMA-reconstruct anti-pattern)
**When:** OpenOnco pilot wave 1, chunk `civic-bma-reconstruct-all` (~1M tokens).
**What:** 95% of the work was a Python script call (`scripts/reconstruct_bma_evidence_via_civic.py` already existed; Phase 3-N had used it for 37 BMAs). Codex spent ~hours on what the script does in seconds.
**Cost:** ~20 Co-Lead-hours pending at upsert step deferred liability. Net-negative even though tokens were "free."
**Drives:** Proposal #1 (Economic Profile required).

### L-2 — strict validator vocabulary blocks legitimate output
**When:** OpenOnco pilot wave 1.
**What:** 4 maintainer-fix PRs in one day (cancer-autoresearch #16, #18, #19, #20). Each was a real validator gap — Codex's legitimate output was rejected:
- `target_action: review_existing_hosted_draft` — invented but valid semantic; validator only had `{upsert, new, flag_duplicate}`.
- Manifest `id::path::filename` triple format — validator treated whole line as one ID.
- `target_entity_id` missing on review actions — validator required it; payload's top-level `id` should fall back.
- Banned-source check unconditional — `SRC-ONCOKB` legacy in faithful snapshots was correctly preserved by Codex but tripped a check that should only fire for write actions.
**Cost:** 4 round-trip cycles in one day; each blocked Codex re-push.
**Drives:** Proposal #2 (permissive-by-default validator).

### L-3 — formal claim ceremony is overhead for trusted agents
**When:** OpenOnco pilot wave 1.
**What:** Codex skipped the formal "open issue → claim → branch" ceremony and pushed branches directly. Maintainer accepted; pipeline worked. The ceremony exists for unknown external contributors.
**Drives:** Proposal #3 (trusted-agent contribution path).

### L-4 — helper scripts in `scripts/` (root) are useful but out-of-spec
**When:** OpenOnco pilot wave 2 (audit chunks).
**What:** Codex wrote `tasktorrent_generate_audit_chunks.py` and `tasktorrent_generate_gap_chunks.py` as helper scripts during chunk execution. Outside `contributions/<chunk-id>/` per current spec.
**Drives:** Proposal #4 (`scripts/contributors/<chunk-id>_*.py` allowed area).

### L-5 — chunk bundling without explicit support
**When:** OpenOnco pilot wave 2 + 3.
**What:** Codex bundled 2 chunks (rec-wording + ua-translation) and 3 chunks (bma-drafting + redflag + source-stub) in single commits. Pragmatic but breaks "one chunk = one PR" rule.
**Drives:** Proposal #5 (explicit bundle support).

### L-6 — manifest format flexibility
**When:** OpenOnco pilot wave 3.
**What:** Codex used `id::path::filename` triples; validator wanted bare IDs.
**Drives:** Proposal #6 (manifest parser accepts multiple formats; cancer-autoresearch PR #20 implements for OpenOnco).

### L-7 — branch-name convention not enforced
**When:** OpenOnco pilot, throughout.
**What:** `tasktorrent/<chunk-id>` was a soft rule. Codex respected; future contributors may not. CI doesn't enforce.
**Drives:** Proposal #7 (branch-name CI gate).

### L-8 — Drop-estimate calibration unknown
**When:** OpenOnco pilot, throughout.
**What:** Estimates ranged 10–15 Drops/chunk; actual contributor token usage never measured/reported.
**Drives:** Proposal #8 (post-execution honesty reports).

### L-8b — audit chunks need triage-pass gate
**When:** OpenOnco pilot waves 2 (rec-wording, ua-translation) + 4 (citation-verify-v2).
**What:** Audit chunks ship findings, not fixes. `suggested_correction`/`suggested_rewording` are meta-descriptions ("Replace X with Y such as Z"; "Requires full UA rewrite by bilingual clinician"). Bulk-apply impossible. Chunk's value = 0 until maintainer walks the triage queue.
- rec-wording-audit: 870 findings → triage backlog.
- ua-translation: 1858 findings → backlog.
- citation-verify-v2: 247 unsupported + 362 unclear + 184 access_blocked → 793-row maintainer queue.
**Cost:** Hidden backlog dressed as completed work. Same dynamic as L-9.
**Drives:** Proposal #8b (audit-followthrough gate).

### L-9 — merged ≠ applied
**When:** OpenOnco pilot, throughout.
**What:** 7 contribution PRs merged to `master`. Looks like progress. Reality: 0 of 7 actually applied to hosted clinical content (sidecars sit in `contributions/`, awaiting Co-Lead signoff). 2700+ audit findings sit as backlog. Dashboard showing "7 merged" hides ~30+ deferred-Co-Lead-hours liability.
**Drives:** Proposal #9 (`application_status` tracking axis).

### L-10 — review profiles vary wildly per chunk type
**When:** OpenOnco pilot, post-mortem.
**What:** Verification cost ranges from 2 hours (citation-verify 10% sample) to 20 hours (BMA-reconstruct 100% Co-Lead) to 1 hour (UA-translate 15% sample). One-size-fits-all "review process" doesn't fit.
**Drives:** Proposal #10 (review-profile taxonomy).

### L-11 — active-cap was wrong number
**When:** OpenOnco pilot, mid-wave.
**What:** Started at 2; bumped to 10 mid-pilot when first wave validated. The right number depends on shelf size and review throughput.
**Drives:** Proposal #11 (active-cap as derived value).

### L-12 — validator should iterate
**When:** OpenOnco pilot wave 1.
**What:** 4 validator-fix PRs surfaced legitimate gaps (L-2). Strict-from-start doesn't accommodate first-batch novelty.
**Drives:** Proposal #12 (permissive-first-batch validator policy).

### L-13 — replace_source needs title-verification rule
**When:** OpenOnco pilot wave 4 (citation-verify-v2 first submission, PR #23).
**What:** 14 of 142 `replace_source` rows mapped a specific RCT to a Source that's NOT the same trial — lexical-match against existing SRC-* IDs landed on semantically-unrelated trials:
- `MAGNITUDE → CHECKMATE-649` (×4) — niraparib+abi prostate vs nivo gastric
- `THOR → POSEIDON` (×4) — erdafitinib FGFR3 urothelial vs durva-treme NSCLC
- `TROPiCS-02 / LATITUDE / KEYNOTE-522 / PACIFIC → general guidelines` — specific RCT replaced with NCCN/ESMO general doc, loses attribution

Plus 4 lexical near-misses (e.g. PAPILLON → CHRYSALIS).

**Fix:** Maintainer reverify script `reverify_citation_replace_source.py` enforces: trial name (extracted from rationale) must appear in target Source's title/notes. After Codex revision: 121/121 replace_source rows pass title-verification.
**Drives:** Proposal #13 (citation-verify-specific validator gate).

### L-14 — scope_note disclaim is a smell
**When:** OpenOnco pilot wave 4 (citation-verify-914-audit v1 vs v2).
**What:** v1 chunk's `scope_note` explicitly said "It does not claim source-level verification for rows where the audit did not provide a concrete SRC-* source to resolve" — yet the chunk's stated mission was source-by-source verification. Result: all 914 rows shipped `support_status: unclear` by definition. v2 chunk required to actually deliver the disclaimed scope. Wasted contributor tokens (v1 ~1M) on triage-restructuring work that the user thought was real verification.
**Drives:** Proposal #14 (scope-disclaim review at chunk-spec submission; if a chunk's scope_note disclaims a key deliverable, the chunk must be split into v1=what's delivered, v2=what's disclaimed BEFORE opening).

### L-15 — false-positive trial-name extraction
**When:** OpenOnco pilot wave 4 post-merge maintainer triage.
**What:** Codex's rationale text for `source_stub_needed` rows uses generic words ("CROSS", "PARADIGM") as if they were trial names. When Codex doesn't have a clear trial in the v1 audit row, it labels something. Maintainer extraction script captured 47 "unique trials" but at least some are false positives (e.g. "CROSS" appearing across 16 unrelated disease domains).
**Drives:** Proposal #15 (downstream-extraction-robustness rule for contributor agent: if no clear trial name in source, return `null`, don't fabricate).

### L-16 — maintainer-side reverify scripts are core infrastructure
**When:** OpenOnco pilot waves 1 + 4.
**What:** `reverify_bma_civic.py`, `reverify_citation_replace_source.py` — these maintainer-side scripts that run independent re-execution of mechanical steps are how the maintainer says "trust the contributor's output without 100% expert review." TaskTorrent reference repo should ship reusable templates for these, especially per chunk-type (computational re-verify for mechanical, sample-verify for semantic).
**Drives:** Proposal #16 (reusable reverify-script templates in TaskTorrent reference).

### L-17 — setuptools flat-layout breaks when `contributions/` lands at top-level
**When:** OpenOnco pilot wave 4 maintainer apply step.
**What:** `pip install -e .` errored with "Multiple top-level packages discovered" because `contributions/` (added by TaskTorrent bootstrap) is a sibling of the actual Python package. KB validator CI broke. Fix: explicit `[tool.setuptools.packages.find]` include/exclude in `pyproject.toml`.
**Drives:** Proposal #17 (TaskTorrent bootstrap should ship pyproject patch / mention this in onboarding doc).

### L-19 — claim coordination has invisible-window risk
**When:** Pilot wave 5 question, post-citation-verify-v2.
**What:** Current claim model has gaps:
- **Open contributor flow** (formal): comment on `[Chunk]` issue → maintainer assigns → assignee field is the lock. Race window between comment and assign.
- **Trusted-agent flow** (Codex): push branch directly. Branch on origin = lock. But invisible window between local-work-start and first-push (could be hours).
- **Cross-chunk manifest overlap**: two chunks with different IDs but overlapping entity manifests aren't auto-detected at issue-open time. `check_manifest_overlap.py` exists but isn't wired to issue-open hook.

**Risks:**
- Two trusted agents both start same chunk locally without push → produce duplicate work.
- Stale claim (14+ days no activity) blocks slot indefinitely.
- Maintainer assigns same chunk to two open contributors during race window.

**Drives:** Proposal #19 (claim-coordination hardening):
- (a) **WIP-branch-first** for trusted agents — push minimal/empty branch immediately at start.
- (b) **Auto-release stale claims** — issue with `assignee` + no commits in 14 days → bot drops assignee.
- (c) **Cross-chunk manifest overlap check at issue-open** — `check_manifest_overlap.py` runs against ALL active chunks.
- (d) **`claim_method` declared in chunk-spec** — `formal-issue` | `trusted-agent-wip-branch-first`.
- (e) **24h assignment SLA** for formal flow — auto-release if maintainer doesn't assign within 24h.

### L-18 — high-volume contribution can break unrelated CI gates (bundle size)
**When:** OpenOnco pilot post-wave 4, applying 399 BMA upsert.
**What:** OpenOnco's `test_engine_bundle_*` tests cap engine bundle at 3MB. Phase 3-N's BMA reconstruction (37 BMAs × ~250 lines each) plus contributor's full 399-BMA upsert pushed the bundle over the limit, failing 5 pre-existing tests. The contribution itself was correct; the side-effect of cumulative volume hit a project-side budget that wasn't surfaced as a chunk-spec acceptance criterion.

**Pattern:** chunks that mutate bulk-volume properties (size, count, refs) of hosted content can trip project-internal budgets (bundle size, render budget, token budget for downstream consumers) that aren't part of TaskTorrent's per-chunk acceptance gates.

**Drives:** Proposal #18 (chunk-spec authors should declare `volume_impact` budget impact when chunk modifies hosted content at scale: `bundle_size_delta`, `entity_count_delta`, etc. + maintainer-side budget gates run on apply, not on contributor PR).

---

## Proposed system changes

Numbered to match lesson IDs. Tier ordering: Tier 1 = ship within 1 week, Tier 2 = within 2-4 weeks, Tier 3 = nice-to-have / iterative.

### Tier 1 (top asks)

**#1 Economic Profile required field.** Add to `chunk-system.md` schema: `compute_profile`, `script_alternative`, `verification_cost`, `break_even_test`. Decision rule: `break_even_test: FAIL` chunks do NOT open. Already done for OpenOnco in PR #14; promote to generic.

**#2 Permissive-by-default validator.** Ship reference validator with extensible `TARGET_ACTIONS` (split into write/review buckets), flexible `MANIFEST_FORMAT` (accept `id` or `id::path::filename`), conditional banned-source check (hard for write, soft for review), `target_entity_id` fallback to payload `id` for review actions.

**#3 Trusted-agent contribution path.** Two contribution flows: open (formal issue-claim) + trusted-agent (push branches directly). Same validator gates apply to both.

### Tier 2

**#8b Audit-followthrough gate.** When `output_type: report-only` AND audit-style, require `audit_followthrough` field: `triage_method`, `triage_rate_committed`, `triage_queue_path`, `triage_status_tracker`. Without it, audit chunk is "shipped but unrealized."

**#9 `application_status` tracking axis.** chunk_status becomes two-axis: `contribution_status` × `application_status`. Dashboards show both. Avoids merged-vs-applied confusion.

**#10 Per-chunk-type review profile taxonomy.** Profiles: `report-automated` / `report-expert-sample` / `entity-write-fullexpert` / `metadata-classification` / `script-replaceable`. Chunk-spec author picks profile; Economic Profile derives.

**#11 Active-cap as derived value.** `active_cap = min(shelf_size, review_capacity_hours_per_week / avg_chunk_review_hours)`. Default a function, not a constant.

**#13 Citation-verify validator gate.** For `replace_source` rows in citation-verify chunks: validate trial name from `verified_rationale` appears in target Source's title/notes. Reference impl: `reverify_citation_replace_source.py`.

**#14 Scope-disclaim review at chunk-spec submission.** If chunk's `scope_note` disclaims a key part of the stated mission, split before opening — don't ship "did the easy half, named it the whole thing."

### Tier 3

**#4 Helper scripts area** (`scripts/contributors/<chunk-id>_*.py`).

**#5 Bundle-PR explicit support** (PR description declares `bundle: [chunk-a, chunk-b]`).

**#6 Manifest format flexibility** (already done in cancer-autoresearch PR #20).

**#7 Branch-name CI gate** (auto-validate `tasktorrent/<chunk-id>`).

**#8 Post-execution honesty reports** (optional `post_execution_metrics` in `_contribution_meta.yaml`).

**#12 Permissive-first-batch validator policy** (Wave 1 = warn-only; Wave 2+ = strict).

**#15 Contributor-agent rule: don't fabricate trial names.** When `verified_rationale` cannot identify a specific trial, return `null` and `suggested_action: maintainer_review`, not a guess that becomes false-positive in downstream extraction.

**#16 Reusable reverify-script templates** (`scripts/tasktorrent/templates/reverify_<chunk-type>.py`) shipped with reference repo.

**#17 pyproject setuptools-find patch** in TaskTorrent bootstrap onboarding doc — when adding `contributions/` at top-level, projects need to update their build config.

**#19 Claim-coordination hardening** — WIP-branch-first for trusted agents; auto-release stale claims after 14 days; cross-chunk manifest overlap check at issue-open; explicit `claim_method` in chunk-spec; 24h assignment SLA for formal flow. See L-19 sub-proposals (a)-(e).

**#18 Chunk volume-impact declaration.** Chunk specs that mutate hosted content at scale (bulk upsert, mass entity creation, rebuild of references) should declare expected `volume_impact` (bundle-size delta, entity-count delta, render-budget delta). Maintainer-side apply step runs project's volume gates BEFORE writing to hosted; surfaces budget breaks as actionable warnings rather than as silent CI failures on the next unrelated PR. OpenOnco's bundle-size budget (3MB) was unrelated to chunk safety but blocked the apply PR — a `volume_impact` declaration would have caught it at apply-time.

---

## Living changelog

| Date | Lesson(s) added | Source event |
|---|---|---|
| 2026-04-28 | L-1..L-12 | OpenOnco pilot wave 1-3 retrospective (PR #15 merged into this doc) |
| 2026-04-28 | L-8b (audit-followthrough) | rec-wording + ua-translation triage queues generated |
| 2026-04-28 | L-13 (replace_source title-verify) | PR #23 first submission had 14 wrong mappings; revision applied |
| 2026-04-28 | L-14 (scope_note disclaim) | citation-verify v1 vs v2 scope-mismatch; v2 chunk-spec written to deliver disclaimed scope |
| 2026-04-28 | L-15 (trial-name false positives) | trial extraction script flagged "CROSS" across 16 unrelated domains |
| 2026-04-28 | L-16 (reverify templates) | reverify_bma_civic + reverify_citation_replace_source written as maintainer infra |
| 2026-04-28 | L-17 (setuptools flat-layout) | KB validator CI broke on PR #22 due to `contributions/` at top-level |
| 2026-04-28 | L-18 (volume-impact declaration) | Bundle-size 3MB budget broke after BMA upsert apply (cumulative Phase 3-N + 399 BMA) |
| 2026-04-28 | L-19 (claim coordination) | Maintainer raised parallel-work risk; gap analysis surfaced 5 mitigations |

When new lessons land, append a row + add the L-N section above + update Tier proposals as needed.

---

## What's NOT in scope

- **Not a TaskTorrent rewrite.** All proposals are additive or governance-level. The chunk model holds.
- **Not OpenOnco-specific.** Each lesson is generalized to apply to any TaskTorrent project.
- **Not a contract.** TaskTorrent owner picks adoption + ordering.
- **Not a substitute for the frozen retrospective docs.** `improvements-from-openonco-pilot.md` and `owner-request-from-openonco-pilot.md` are the timestamped initial reports. This doc is the living plan that builds on them.

---

## Linked source artifacts

- **Chunk specs (with retroactive Economic Profile):** `chunks/openonco/*.md`
- **Decision tree:** `docs/script-vs-chunk-decision.md`
- **Initial retrospective:** `docs/improvements-from-openonco-pilot.md`
- **Owner ask letter:** `docs/owner-request-from-openonco-pilot.md`
- **Validator + reverify scripts (live):** `cancer-autoresearch/scripts/tasktorrent/*.py`
- **Sample triage queues (live):** `cancer-autoresearch/contributions/*/triage-queue-*.md`
