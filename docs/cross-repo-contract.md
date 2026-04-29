# Cross-Repo Contract — task_torrent ↔ consumer repos

**Status:** v0.4 canonical. Lives in `task_torrent/docs/cross-repo-contract.md`. Consumer repos may mirror it as `docs/contributing/cross-repo-contract.md` with frontmatter `synced_from: task_torrent@main#docs/cross-repo-contract.md`.

**Audience:** consumer-repo maintainers (e.g. OpenOnco's), contributor agents, and anyone writing tooling that bridges the two sides.

This doc is the **shared contract** that lets a contributor's AI tool find a chunk on a consumer repo, claim it, work it, and submit a PR — without the contributor's tool having to know which consumer it's working with. The contract is small, structured, and stable across consumers.

## Parties

```
task_torrent (rules-repo)
  ├── chunk-system spec
  ├── lint_chunk_spec.py (canonical contract enforcement)
  ├── chunks/<consumer-name>/<chunk-id>.md (chunk specs)
  └── this doc

consumer repo (e.g. romeo111/OpenOnco)
  ├── .github/ISSUE_TEMPLATE/tasktorrent-chunk-task.md
  ├── scripts/tasktorrent/ (next_chunk.py, auto_claim.sh, auto_pr.sh, validate_contributions.py, …)
  ├── contributions/<chunk-id>/ (sidecars from contributors)
  └── (optional) mirror of this doc

contributor agent (Claude Code, Codex, …)
  └── reads from both repos via gh + git
```

## Discovery contract

**Query:** consumer repo's GitHub Issues, filtered by:
- `labels=chunk-task,status-active`
- `assignee=none`
- `state=open`

**Pick:** oldest first (FIFO). This pressures stale-claim release before new claims pile on.

Reference implementation: `cancer-autoresearch/scripts/tasktorrent/next_chunk.py`.

## Issue-body contract

When a consumer maintainer opens a chunk-task issue, the body uses the consumer's `.github/ISSUE_TEMPLATE/tasktorrent-chunk-task.md`. The body **must** include these `## ` headings, in any order, parseable by `next_chunk.py`:

| Heading | Content | Format |
|---|---|---|
| `## Chunk Spec` | URL of the chunk-spec markdown in `task_torrent/chunks/<consumer>/<chunk-id>.md` | first https URL on the line |
| `## Chunk ID` | the stable chunk identifier | first inline `code` token |
| `## Topic Labels` | comma-separated topic labels for filtering | inline `code` tokens |
| `## Drop Estimate` | token budget | text including "~N Drops" or "~Xk tokens" |
| `## Required Skill` | link to a skill spec in `task_torrent/skills/` | first inline `code` token |
| `## Branch Naming Convention` | branch name format | inline `code` token, format `tasktorrent/<chunk-id>` |
| `## Sidecar Output Path` | where contributor sidecars land | first fenced codeblock body |
| `## Claim Method` | one of: `formal-issue`, `trusted-agent-wip-branch-first` | first inline `code` token |
| `## Task Manifest` | concrete entity IDs / file paths | fenced codeblock or bullet list |
| `## Allowed Sources` | which sources may be cited | prose |
| `## Disallowed Sources` | which sources are banned (consumer-side) | prose |
| `## Acceptance Criteria (machine-checkable)` | machine-verifiable checks | unchecked-box list |
| `## Acceptance Criteria (semantic, maintainer-checked)` | maintainer-verifiable checks | unchecked-box list |

Headings exactly as shown. The parser tolerates `## Branch Naming` as an alternate for `## Branch Naming Convention`.

## Chunk-spec contract

The chunk-spec markdown (in `task_torrent/chunks/<consumer>/<chunk-id>.md`) is the **single source of truth** for the chunk's content. The issue body is a UI summary that points to the spec.

The chunk-spec is validated by `tasktorrent/lint_chunk_spec.py`. Required sections:

```
Status, Topic Labels, Mission, Economic Profile, Drop Estimate,
Required Skill, Allowed Sources, Manifest, Output Format,
Acceptance Criteria, Rejection Criteria, Claim Method
```

**Conditional sections:**
- MARGINAL chunks (Economic Profile `break_even_test: MARGINAL`) must declare `expected_violations` (Proposal #20 / L-20).
- Volume-mutating chunks must declare `volume_impact` (Proposal #18 / L-18).

The linter is a `pip install`-able package (`tasktorrent>=0.4`). Consumer CI should run it on every PR that touches `chunks/*.md`.

## Claim contract

**`formal-issue`** flow:
1. Contributor comments on the issue: `I'd like to take this chunk.`
2. Maintainer assigns within 24h SLA (claim-sla-bot enforces; auto-releases if missed).
3. Contributor begins work on `tasktorrent/<chunk-id>` branch.

**`trusted-agent-wip-branch-first`** flow:
1. Contributor pushes empty WIP commit to `tasktorrent/<chunk-id>` on origin **immediately when starting**.
2. The branch on origin is the visible lock — other agents see it and don't duplicate.
3. No issue comment required.

**Stale-claim auto-release:** if the assignee/branch goes silent for 14 days, the bot releases the assignee back to the shelf. Reference impl: `cancer-autoresearch/scripts/tasktorrent/auto_release_stale_claims.py`.

## Sidecar contract

Contributor work lands under `contributions/<chunk-id>/` in the consumer repo. Required files:

| File | Required | Content |
|---|---|---|
| `_contribution_meta.yaml` | yes | `chunk_id`, `contributor`, `submission_date`, `ai_tool`, `ai_model`, optional `ai_model_version`, `ai_session_notes` |
| `task_manifest.txt` | yes | the manifest entries from the issue, one per line |
| sidecar YAMLs | per chunk | one file per entity; field shape per chunk-spec |

**Allowlist enforcement:** `git diff --name-only base..HEAD` must list **only** files under `contributions/<chunk-id>/`. Anything outside is a `scope` rejection (per dispute-resolution vocabulary in `protocol-v0.4-design.md` §"Owner-resolved decisions").

**`_contribution.target_action`** vocabulary: `new`, `upsert`, `flag_duplicate`, `review_existing_hosted_draft`, `review_existing_stub` (the latter two for review-only sidecars per L-2 / Proposal #2).

**Optional fields** (per owner decision 2026-04-28 / Proposal #27):
- `_contribution.tasktorrent_version` — observability-only commit hash, no enforcement
- `_contribution.cost_actual` — `tokens` / `model` / `usd` for token-economy tracking

## Rejection-code vocabulary

When a maintainer rejects a contributor PR, the comment must include a `rejection_code:` line drawn from this controlled vocabulary (per `protocol-v0.4-design.md` Gap 3 owner decision):

| Code | Meaning |
|---|---|
| `schema` | Output failed Pydantic / format validation |
| `manifest` | Sidecar entity ID outside the chunk's manifest |
| `source-policy` | Banned source used, or licensing classification wrong |
| `quality` | Output formally valid but content-incorrect |
| `safety` | Crosses safety boundary (medical advice, patient data, etc.) |
| `scope` | Outside the chunk's stated scope |
| `economics` | Token cost vastly above estimate without justification |
| `duplicate` | Work overlaps another in-flight or merged chunk |
| `stale-claim` | Claim expired before submission; chunk re-released |

Contributors may open an appeal issue tagged `tasktorrent-appeal` referencing the rejection code; appeals triage within 7 days.

## Banned sources (per consumer)

Consumers declare their own banned-sources list in the issue template's `## Disallowed Sources` section. OpenOnco's list:

- `SRC-ONCOKB` — OncoKB (CHARTER §2 ToS conflict with non-commercial use)
- `SRC-SNOMED` — SNOMED CT (license gate)
- `SRC-MEDDRA` — MedDRA (license gate)

The `validate_contributions.py` reference implementation reads the consumer's banned list from chunk-spec / config + applies a hard gate. New consumers customize via `.tasktorrent.yaml.banned_sources` (when adopted).

## Versioning contract (v0.4: first public release)

- task_torrent v0.4.0 is the first tagged public release.
- Consumer repos **do not** require `.tasktorrent.yaml` version pin in v0.4.
- Sidecars **may** include optional `_contribution.tasktorrent_version` (tag or commit-hash style, e.g. `v0.4.0` or `2026-04-29-abc1234`) for post-hoc drift trace.
- Breaking changes ride a two-release deprecation window per `protocol-v0.4-design.md` Gap 2: vN warn → vN+1 error → vN+2 remove.
- Each breaking-change release ships a `MIGRATION.md` block in the changelog.

This means consumers and contributors operate on `main` of task_torrent. If a breaking change lands, contributors with old `tasktorrent_version` stamps still validate (legacy-grace), but new sidecars must comply.

## Trust tiers (consumer-side)

Per `protocol-v0.4-design.md` Gap 1:

- **T0** — anonymous / first-time. `formal-issue` only. Full review per PR.
- **T1** — track-record contributor (≥3 merged chunks for this consumer, **zero safety / source-policy violations**, zero rejections in last 90 days). Either claim flow. Sample-based review.
- **T2** — co-maintainer. Manually granted.

Tiers are **per-consumer-repo, not portable** by default. Cross-repo trust registry is opt-in (`trust_registry.honor: true` in `.tasktorrent.yaml`).

## Reference implementations

| Component | Location | Purpose |
|---|---|---|
| `next_chunk.py` | `cancer-autoresearch/scripts/tasktorrent/` | Issue-body parser, JSON emitter |
| `auto_claim.sh` | same | claim per declared method |
| `auto_pr.sh` | same | pre-flight + open PR |
| `bootstrap_contributor.sh` | same | discover + orient |
| `validate_contributions.py` | same | sidecar gate |
| `lint_chunk_spec.py` | `task_torrent/tasktorrent/` | chunk-spec lint |
| `claim-sla-bot` | `cancer-autoresearch/scripts/tasktorrent/check_claim_sla.py` + workflow | hourly 24h-SLA enforcer |
| `stale-claim-bot` | `cancer-autoresearch/scripts/tasktorrent/auto_release_stale_claims.py` + workflow | daily 14d sweep |

A new consumer adopts the contract by copying these reference implementations + customizing the banned-sources list and KB allowlist.

## Living document

This contract evolves via PRs to this file in `task_torrent`. Breaking changes follow the two-release deprecation discipline (`protocol-v0.4-design.md` Gap 2). Non-breaking additions land directly. Consumers that mirror this doc should re-pull on each landed change.

Open questions tracked in `docs/protocol-v0.4-design.md` "Owner-resolved decisions" section.
