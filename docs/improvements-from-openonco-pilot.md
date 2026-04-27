# TaskTorrent Improvements: Lessons from OpenOnco First Pilot

This document is for **TaskTorrent maintainers**. It generalizes the lessons from the OpenOnco first-pilot wave (4 chunks completed in 1 day, 4 maintainer-fix PRs surfaced during review, 1 chunk classified retroactively as economically-FAIL) into proposed changes to the TaskTorrent system itself.

These recommendations are project-agnostic. OpenOnco-specific encoding lives in `docs/openonco-pilot-workflow.md`.

## Pilot summary

- **4 chunks executed** by Codex agent (one bundled commit covered 2 chunks; one bundled covered 3): civic-bma-reconstruct-all (399 BMA), citation-verify-914-audit (914 rows), rec-wording-audit-claim-bearing + ua-translation-review-batch, bma-drafting-gap-diseases + redflag-indication-coverage-fill + source-stub-ingest-batch
- **~4M tokens contributor work** on the three commits
- **4 validator-fix PRs** (#16, #18, #19, #20) surfaced real bugs in the maintainer-side checks
- **1 chunk retroactively FAIL** — civic-bma-reconstruct-all should have been a script (`scripts/reconstruct_bma_evidence_via_civic.py` already existed)
- **Active-cap: bumped from 2 → 10** mid-pilot once the pipeline validated

## Top 3 system-level changes

### 1. Economic Profile as a system primitive (not just per-project)

**Observation:** the chunk-spec template required mission, manifest, output format, etc. It did NOT require any economic justification. Result: contributors could open chunks for work that was net-negative under maintainer review burden, even though contributor tokens were "free."

**Proposed change:** make Economic Profile a top-level required field in the canonical `chunk-system.md` (already done for OpenOnco in PR #14 — promote to generic).

```yaml
## Economic Profile

compute_profile: mechanical | llm-essential | mixed
llm_essential_pct: <0–100>
script_alternative:
  exists: yes | no | partial
  path: scripts/foo.py | null
  rationale: >

verification_method: automated | sample | full-expert-review | mixed
verification_cost:
  maintainer_hours: <number>
  expert_hours: <number>      # generic field; project specifies expert specialty
  expert_specialty: ""

break_even_test: PASS | MARGINAL | FAIL
break_even_rationale: >
```

**Decision rule:** chunks with `break_even_test: FAIL` do NOT open. They become script work.

**Impact:** prevents the most common pilot failure mode (chunk-as-script-substitute).

### 2. Validator: permissive-by-default + extensible vocabulary

**Observation:** strict validator with hardcoded `target_action ∈ {upsert, new, flag_duplicate}` rejected legitimate Codex submissions that introduced `review_existing_hosted_draft`. Same with manifest format (bare-ID vs `id::path::filename`). Same with banned-source check (banned everywhere vs banned-only-for-write-actions). Each surfaced as a maintainer fix PR during real review.

**Proposed change:** ship the reference validator as **permissive-by-default**, with all gates explicitly extensible:

```python
# chunk-validator config (TaskTorrent reference impl)
TARGET_ACTIONS = {
    "write": ["upsert", "new"],            # require target_entity_id
    "review": ["flag_duplicate", "review_existing_hosted_draft", "review_existing_stub"],
    # extensible — projects add tokens via config
}

ENTITY_SIDECAR_PREFIXES = ("bma_", "bio_", "drug_", "ind_", "source_stub_")  # project-overridable

MANIFEST_FORMAT = "id-or-id-path-triple"  # parse `id` OR `id::path::filename`

BANNED_SOURCE_CHECK = {
    "write_actions": "hard",   # reject for upsert/new
    "review_actions": "soft",  # warn but accept (faithful snapshot of legacy)
}
```

**Impact:** first-batch contributors don't trip on artificial validator limits; new vocabulary is added via config, not hardcoded.

### 3. Trusted-agent contribution path

**Observation:** Codex (the OpenOnco-pilot's first contributor) skipped the formal "open issue → claim → branch" ceremony and just pushed branches directly. Maintainer accepted; pipeline worked. The formal ceremony is for ANONYMOUS external contributors, not for known agents the maintainer pre-authorized.

**Proposed change:** add two explicit contribution paths to the chunk-system spec:

- **Open path** — formal `[Chunk]` issue → claim → branch. For external/unknown contributors. Default for shelf chunks.
- **Trusted-agent path** — maintainer pre-authorizes a contributor (e.g. their own Codex agent or a known partner). Contributor pushes branches directly. Maintainer reviews PR; same validator gates apply. No issue-claim ceremony.

The validator gates protect both paths equally. The ceremony is governance, not safety.

**Impact:** removes friction for trusted high-throughput contributors without weakening safety.

## Medium-priority changes

### 4. Helper scripts area (`scripts/contributors/`)

**Observation:** Codex wrote `tasktorrent_generate_audit_chunks.py` and `tasktorrent_generate_gap_chunks.py` as helper scripts during chunk execution. These ended up in `scripts/` (root) — useful artifacts but technically out of scope per "all output goes to `contributions/`" rule.

**Proposed change:** explicitly allow `scripts/contributors/<chunk-id>_*.py` as a valid output path. Update validator scope check accordingly.

### 5. Bundled-chunks explicit support

**Observation:** Codex bundled 2 then 3 chunks in single commits. "One chunk = one PR" rule was technically violated but pragmatically fine. Bundling shares manifests, helper scripts, and reduces PR ceremony.

**Proposed change:** allow `bundle: [chunk-a, chunk-b]` in PR description. Validator runs against each chunk's directory separately. Maintainer can merge or split bundle as appropriate.

### 6. Manifest format flexibility (already done in #20)

Generic spec: validator accepts bare IDs OR `id::path::filename` triples. Take first `::`-separated field as canonical ID. Already in OpenOnco's validator; should be in the reference impl.

### 7. Branch-name CI gate

**Observation:** branch naming convention `tasktorrent/<chunk-id>` was a soft rule. CI didn't enforce. Codex respected it; future contributors may not.

**Proposed change:** ship a CI workflow snippet that validates branch name matches `tasktorrent/<chunk-id>` (project may extend pattern). Auto-reject if not.

### 8. Post-execution honesty reports

**Observation:** chunk-spec Drop-estimates were never validated against actual contributor token usage. We don't know if 12-Drop chunk actually used 1.2M tokens or 600k or 2M.

**Proposed change:** add optional fields to `_contribution_meta.yaml`:

```yaml
post_execution_metrics:
  actual_tokens_used: <number, contributor reports>
  actual_runtime_minutes: <number>
  actual_llm_essential_pct: <number, retroactive estimate>
  contributor_self_assessment: smooth | rough | needs-rework
```

Aggregate across chunks → calibrate future Drop estimates.

## Strategic changes

### 9. Track merged-vs-applied

**Observation:** the OpenOnco pilot has 7 merged contribution PRs. ZERO have been upserted into `hosted/content/` yet (Co-Lead signoff queue). The chunk's value is realized only on apply — until then, it's a deferred liability (review hours owed).

**Proposed change:** TaskTorrent reference docs distinguish `chunk_status` two-axis:

```
chunk_status:
  contribution_status: queued | active | merged | rejected
  application_status:  pending | applied | dropped
```

A chunk is "complete" only when `applied`. Dashboards / shelf views must show both axes. Avoids the "we shipped 7 chunks!" optimism that hides 7 unapplied backlogs.

### 10. Per-chunk-type review profiles (codify the matrix)

**Observation:** OpenOnco pilot showed wildly different review costs:

- citation-verify: 10% sample = 2 hours
- bma-drafting: 100% Co-Lead = 5 hours
- ua-translate: 15% UA-clinician = 1 hour
- BMA-reconstruct: 100% Co-Lead = 20 hours pending

**Proposed change:** TaskTorrent reference docs ship a "review profile" taxonomy:

| Profile | Sample % | Expert role | Typical chunk size |
|---|---|---|---|
| `report-automated` | 10% | maintainer | 1M tokens |
| `report-expert-sample` | 15% | specialty expert | 1M tokens |
| `entity-write-fullexpert` | 100% | claim-domain expert | <500k tokens |
| `metadata-classification` | 20% | maintainer | 1M tokens |
| `script-replaceable` | N/A | DO NOT CHUNK | N/A |

Chunk-spec authors pick a profile. The economic profile derives from it.

### 11. Active-cap is a derived value, not a fixed config

**Observation:** OpenOnco started cap=2, bumped to 10 mid-pilot. The "right number" depends on shelf size + review throughput.

**Proposed change:** active-cap should be DERIVED:

```
active_cap = min(
    shelf_size,                                # can't run more than exist
    review_capacity_hours_per_week / avg_chunk_review_hours
)
```

Recommendation in chunk-system.md: make `active_cap` a function, not a constant. Default function = above formula.

### 12. Validator "permissive first batch" → "tighten after wave 1"

**Observation:** during pilot we discovered 4 validator gaps. Each cost a maintainer-fix PR and a contributor-rebase cycle.

**Proposed change:** explicit two-phase validator policy:

- **Wave 1 (first N chunks of a project):** validator runs in `permissive` mode — warns but doesn't reject on novel patterns. Maintainer reviews warnings and decides if pattern is valid (adds to vocab) or genuine bug (asks contributor to fix).
- **Wave 2+ (after vocab settles):** validator runs in `strict` mode — rejects on any pattern not in vocab.

This avoids the "contributor blocked → maintainer rushes a fix PR" cycle that we hit 4× during pilot.

## Implementation order (recommendation)

Tier 1 (do first):
- #1 Economic Profile required field (already done for OpenOnco; promote to generic)
- #2 Permissive validator (extensible vocab, configurable gates)
- #3 Trusted-agent path (governance distinction)

Tier 2 (do second):
- #9 merged-vs-applied tracking (reframes "completion")
- #10 review profiles (codifies expert-time costs)
- #11 active-cap as derived value

Tier 3 (do as needed):
- #4–#8 (manifest formats, helper scripts, bundling, branch CI, honesty reports)
- #12 (permissive-first-batch validator policy — an evolution of #2)

## What this is NOT

- **Not a rewrite of TaskTorrent.** All proposals are additive or governance-level. The core model (chunk = unit of LLM-essential work) holds.
- **Not OpenOnco-specific.** Each proposal is generic to any project using TaskTorrent. OpenOnco is just the example dataset.
- **Not a contract.** TaskTorrent maintainers decide which proposals to adopt, when, and in what form.

## Source data

This document derives from:

- `chunks/openonco/*.md` post-pilot (with retroactive Economic Profile fills)
- `docs/script-vs-chunk-decision.md` (OpenOnco pilot's anti-patterns)
- 4 maintainer-fix PRs in cancer-autoresearch: #16, #18, #19, #20
- 5 contribution PRs in cancer-autoresearch: #14, #15, #17, #21 (and rebased predecessors #9, #10)

Data is current to 2026-04-28.
