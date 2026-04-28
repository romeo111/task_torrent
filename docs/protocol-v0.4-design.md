# TaskTorrent Protocol v0.4 — design doc

**Status:** draft — written 2026-04-28, acting in owner capacity at OpenOnco maintainer's invitation. Not yet ratified.

**Scope:** structural protocol additions between the three parties of TaskTorrent (rules-repo, consumer projects, contributors). Sits on top of the lessons-and-proposals improvement plan (`docs/tasktorrent-improvement-plan.md`); does not replace it.

**Why a separate doc:** the improvement plan tracks specific lessons from one pilot. This doc proposes structural contracts that determine whether TaskTorrent generalizes from "OpenOnco's coordination layer" to "any social-good project's coordination layer."

---

## The three parties

| Party | Today's role | Today's authority |
|---|---|---|
| **task_torrent (rules-repo)** | Owns chunk-system spec, skill specs, issue template, validator contract | Whatever `main` says, right now |
| **Consumer project** (e.g., OpenOnco) | Owns its KB, its validators, its sidecars, its CI gates | Sets banned-sources, active-cap, review profile |
| **Contributor** (Codex, Claude, human) | Claims chunks, executes, opens PRs | Tied to GitHub identity; trust is implicit |

The protocol gaps below all stem from one root: **the contracts between these parties are implicit**. Implicit contracts work with one consumer + one trusted contributor. They don't scale.

---

## Gap 1 — trust model is undefined

### Problem

`trusted-agent-wip-branch-first` claim flow exists, but "trusted" has no operational definition. Who's pre-authorized? How does a contributor become trusted? How does trust get revoked? Today: by maintainer DM, ad-hoc.

This blocks N>1 consumers because each consumer must hand-curate its trusted-agent list with no shared signal.

### Design — three-tier trust model

**Tiers:**

| Tier | Eligibility | Claim flow | Review depth |
|---|---|---|---|
| **T0** anonymous / first-time | New GitHub identity for this consumer | `formal-issue` only | Full end-to-end review per PR |
| **T1** track-record contributor | ≥3 merged chunks for this consumer, zero rejections in last 90 days | `formal-issue` OR `trusted-agent-wip-branch-first` | Sample-based review; reverify scripts run; full review on flagged outputs |
| **T2** co-maintainer | Manually granted by existing maintainers | Either flow + can open chunks + can run apply scripts | Self-review allowed for mechanical chunks; semantic chunks require second maintainer |

Tiers are **per-consumer-repo**, not portable by default.

### Trust ledger

Each consumer repo keeps `.tasktorrent/contributors.yaml`:

```yaml
contributors:
  - github: codex-ai
    tier: T1
    merged_chunks: 7
    rejections_90d: 0
    last_action: 2026-04-28
    granted_by: romeo111
  - github: claude-opus-4-7
    tier: T1
    merged_chunks: 3
    ...
```

Auto-updated by a workflow on PR merge / rejection. Tier transitions:
- **T0 → T1** automatic at threshold (configurable per consumer; default `merged_chunks >= 3 AND rejections_90d == 0`).
- **T1 → T0** automatic on rejection (configurable cooldown).
- **anything → T2** PR-only by existing T2.

### Cross-repo portability (optional)

task_torrent maintains an opt-in registry: `task_torrent/contributors-registry.yaml` listing T1+ contributors with consumer references. New consumer repos can configure:

```yaml
# .tasktorrent.yaml (consumer-side)
trust_registry:
  honor: true              # default false — every consumer earns its own trust
  min_consumer_count: 2    # only honor if contributor has T1 in ≥N other consumers
```

Default is **don't honor**. Consumers opt in once they trust the registry maintainer's signal.

### Revocation

Maintainer comments on PR or issue: `@tasktorrent-bot demote <user> <reason>`. Bot updates ledger; future PRs revert to T0 review until manually restored.

### Why this matters

Without it: "trusted-agent" is a vibe; each new consumer hand-curates from scratch.
With it: a contributor that did 5 clean chunks for OpenOnco onboards on a sister project at T1 by default (if registry honored), or earns T1 in the new consumer in ~2 weeks at T0 pace. Time-to-trust drops from "manual decision per agent per consumer" to "merged-PR count crossing a threshold."

---

## Gap 2 — schema evolution is unilateral

### Problem

Today: task_torrent owner changes a rule (e.g., adds required `claim_method` field, narrows a vocabulary, renames a manifest format) → consumers either update or break. PR #18 raised this for version pinning (L-21). But pinning alone isn't enough — without deprecation discipline, consumers will lag forever and eventually upgrade by force.

### Design — two-release deprecation window

Every breaking change to chunk-spec, issue-template, validator contract, or skill spec rides a **two-release deprecation window**:

| Release | New field/rule status | Old field/rule status | Validator behavior |
|---|---|---|---|
| **vN** (introduce) | Optional; warning if absent | Still works | Warn on missing new; warn on present old |
| **vN+1** (require) | Required; error if absent | Deprecated; warning | Error on missing new; warn on present old |
| **vN+2** (cleanup) | Required | Removed; error if present | Error on either |

Consumers see two consecutive releases of warnings before things break. They can pin to vN, see the warnings, plan migration, bump to vN+1 on their schedule.

### Migration manifests

Every release tag ships `MIGRATION.md` containing:

```markdown
## v0.3 → v0.4

### Breaking changes (require migration before vN+1 = v0.5)

- `_contribution_meta.tasktorrent_version` — newly required
  - **Migration:** add `tasktorrent_version: v0.4` to every sidecar
  - **Automated:** `python -m tasktorrent.migrations.v0_3_to_v0_4`

- `chunk-spec.claim_method` — vocabulary narrowed
  - **Old:** any string
  - **New:** {`formal-issue`, `trusted-agent-wip-branch-first`}
  - **Migration:** rewrite chunk specs that use other values
  - **Automated:** none (manual review)

### Non-breaking additions
- `chunk-spec.expected_violations` (Proposal #20) — optional, no migration needed
```

### Automated migration scripts

Mechanical changes (rename, restructure) ship with `task_torrent/migrations/<from>-to-<to>.py` that consumers run locally:

```
python -m tasktorrent.migrations.v0_3_to_v0_4 --repo /path/to/consumer --dry-run
python -m tasktorrent.migrations.v0_3_to_v0_4 --repo /path/to/consumer --apply
```

Consumer commits the diff under version control. Maintainer reviews + merges as a normal PR.

### Why this matters

Without it: every task_torrent bump risks N consumer fires; consumers respond by never bumping; protocol fragments.
With it: bump → consumers see warnings → migrate on their schedule → if they lag, they get warnings, not breaks.

---

## Gap 3 — no consumer-onboarding template

### Problem

Each new consumer ("any other social service") must currently:

- Read chunk-system.md and skill specs
- Lift cancer-autoresearch's validator + adapt
- Lift the issue template + adapt
- Author its own contributor + maintainer docs
- Author its own reverify script templates per chunk archetype
- Stand up CI workflows (claim bots, validator)

That's a 1-2 day setup minimum. First consumer (OpenOnco) did it; second consumer should not redo it from scratch.

### Design — three-piece onboarding kit

**Piece 1: scaffold command.** `tasktorrent init <consumer-name>` (cookiecutter-style) drops a working TaskTorrent setup into any repo:

```
<consumer-repo>/
├── .tasktorrent.yaml                              # version pin, active-cap, defaults
├── scripts/tasktorrent/
│   ├── validate_contributions.py                  # reference impl
│   ├── upsert_contributions.py                    # reference impl, --confirm gated
│   ├── check_manifest_overlap.py
│   ├── check_claim_sla.py                         # L-19 (b)
│   ├── auto_release_stale_claims.py               # L-19 (c)
│   ├── lint_chunk_spec.py                         # see Piece 3
│   └── templates/
│       ├── reverify_mechanical.py
│       ├── reverify_semantic_sample.py
│       └── reverify_audit_report.py
├── .github/
│   ├── ISSUE_TEMPLATE/tasktorrent-chunk-task.md
│   └── workflows/
│       ├── tasktorrent-validate.yml
│       └── tasktorrent-claim-bots.yml
├── docs/contributing/
│   ├── CONTRIBUTOR_QUICKSTART.md
│   └── MAINTAINER_CHUNK_OPENING.md
├── chunks/
│   └── _example.md                                # reference chunk-spec
└── contributions/.gitkeep
```

After running `init`, consumer customizes:
- `.tasktorrent.yaml`: banned-sources, active-cap, review-profile defaults
- `chunks/`: their actual chunk-specs

**Piece 2: `.tasktorrent.yaml` — consumer config contract.**

```yaml
# Required
version: v0.4                  # task_torrent rules version this repo targets
consumer_name: openonco
banned_sources: [SRC-ONCOKB, SRC-SNOMED, SRC-MEDDRA]

# Active-cap — see Proposal #11
active_cap:
  mode: derived                # or `fixed: 10`
  review_capacity_hours_per_week: 40
  avg_chunk_review_hours: 4

# Trust model — see Gap 1
trust_tier_thresholds:
  T0_to_T1:
    merged_chunks: 3
    rejections_90d: 0
trust_registry:
  honor: false

# Volume gates — Proposal #18
volume_gates:
  bundle_size_mb: 3
  entity_count: 10000

# Where the consumer's KB lives
kb_root: knowledge_base/hosted/content/
```

**Piece 3: chunk-spec linter.** Standalone script `tasktorrent/lint_chunk_spec.py` validates any `chunks/<chunk-id>.md` against schema. Required sections:

- Manifest (real entity IDs, not placeholder)
- Economic Profile with `break_even_test: PASS|MARGINAL` (FAIL chunks rejected at lint)
- `claim_method`
- Drop-estimate
- `allowed_sources` and `disallowed_sources` (latter merges with `.tasktorrent.yaml` banned_sources)
- For MARGINAL chunks: `expected_violations` (Proposal #20)
- For volume-mutating chunks: `volume_impact` declaration (Proposal #18)

Consumer CI runs the linter on every PR touching `chunks/*.md`. Chunk-specs that fail the lint can't be promoted to `status-active`.

### Why this matters

Without it: time-to-first-chunk for consumer #2 is days. With it: an afternoon. The protocol becomes reusable, not a one-off case study. The scaffold also encodes the proposal decisions (Economic Profile, claim_method, version pinning, volume gates) into the default setup — so consumer #2 inherits the lessons of OpenOnco automatically.

---

## Adoption sequence

Smallest-first, lowest blast-radius first:

1. **Chunk-spec linter (Piece 3)** — new script, no breaking change. Ship as standalone in task_torrent; consumers adopt by copying. Cost: ~half-day. Immediate value: catches under-specified chunks before they open.

2. **Schema deprecation discipline (Gap 2)** — process change, no code beyond MIGRATION.md template. Cost: discipline, not engineering. Apply starting with the next breaking change after v0.4.

3. **`.tasktorrent.yaml` consumer config (Piece 2)** — new file format + validator reads from it. Cost: ~1 day. Consumer migrates manually; OpenOnco first.

4. **Trust ledger (Gap 1)** — `.tasktorrent/contributors.yaml` schema + bot to update on PR merge. Cost: ~1-2 days. Per-consumer first; cross-repo registry deferred.

5. **`tasktorrent init` scaffold (Piece 1)** — last, because it bakes the four preceding decisions into the template. Cost: ~2-3 days. Validates the protocol by onboarding consumer #2.

Total: ~one week of focused work to get the protocol from "OpenOnco's coordination layer" to "reusable across social-good projects."

---

## What this is NOT

- **Not a contract.** task_torrent owner decides what to adopt and in what order. This is a design proposal, not policy.
- **Not OpenOnco-specific.** Each design generalizes by construction; OpenOnco's specifics are factored into `.tasktorrent.yaml`.
- **Not a replacement for the improvement plan** (L-1..L-21). The improvement plan is lessons-from-one-pilot; this is structural-additions-for-N-pilots.
- **Not a rewrite.** The chunk model holds. Manifests, sidecars, validators all stay. This adds layers above and around the existing core.

---

## Open questions (for owner / multi-consumer review)

1. **Trust registry custody.** If task_torrent maintains a cross-repo trust registry, who's accountable for its accuracy? Per-consumer maintainers report? Bot scrapes PR-merge events?

2. **Contributor cost transparency.** Should the protocol surface token cost / $-spent estimates per chunk? Today the externality (contributor pays compute) is invisible to consumers. Adding a `cost_estimate` field in chunk-spec + a `cost_actual` field in `_contribution_meta.yaml` would make the economy visible — useful for planning but maybe scope-creep for v0.4.

3. **Dispute resolution.** What's the appeal path when a maintainer rejects a PR the contributor believes was correct? Today: nothing. v0.4 could add: rejection codes + optional appeal-issue + lessons captured in MIGRATION.md / improvement plan.

4. **Active-cap derivation formula.** Proposal #11 (active-cap as derived value) needs a real formula. The straw-man in `.tasktorrent.yaml` above (`review_capacity / avg_chunk_review`) ignores chunk-type heterogeneity. May need per-review-profile weighting.

These are flagged for discussion, not designed in this draft.

---

## Linked artifacts

- **Lesson L-21** (cross-repo version pinning) in `docs/tasktorrent-improvement-plan.md` — feeds Gap 2
- **Proposal #19** (claim coordination) in same doc — feeds Gap 1's `formal-issue` vs `trusted-agent` distinction
- **Proposal #11** (active-cap derived) — feeds `.tasktorrent.yaml` config schema
- **OpenOnco's reference implementation** at `cancer-autoresearch/scripts/tasktorrent/` — source for scaffold's reference scripts
