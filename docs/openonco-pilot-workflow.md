# OpenOnco Pilot Workflow

This document is the operational layer between TaskTorrent's general chunk model and OpenOnco's actual repo conventions. OpenOnco has stricter clinical-content review rules than the generic TaskTorrent pilot assumes (CHARTER §6.1 two-Clinical-Co-Lead signoff for `knowledge_base/hosted/content/`, pre-commit Pydantic validation, multi-agent coordination protocol). This doc names the rules so contributors don't trip them.

If anything here conflicts with the OpenOnco repo's `CLAUDE.md`, `specs/CHARTER.md`, or `specs/SOURCE_INGESTION_SPEC.md`, the OpenOnco source-of-truth wins.

## Chunk size and active-cap

- **Minimum chunk size: ~1M tokens (~10 Drops).** Smaller tasks should be done by maintainers directly or as scripts — TaskTorrent ceremony only pays for itself at chunk-scale work.
- **Maximum active chunks: 10.** Raised from initial 2 after the first wave validated the pipeline (4 chunks merged cleanly in one day). At 10 active, cap is effectively non-binding for the current 7-chunk shelf — re-tighten if review throughput becomes the bottleneck.
- **One chunk = one contributor = one PR = one review.**

This bounds reviewer load: at any moment, at most 2 large submissions can be on the maintainer's plate.

## Sidecar workflow (do not edit hosted content directly)

Contributor PRs **do not** edit files under `knowledge_base/hosted/content/`. They write **sidecar files** under a new top-level `contributions/` tree:

```
contributions/
  <chunk-id>/
    bma_<biomarker>_<variant>_<disease>.yaml
    bio_<biomarker>.yaml
    drug_<drug>.yaml
    ind_<indication>.yaml
    source_stub_<src_id>.yaml
    citation-report.yaml
    audit-report.yaml
    task_manifest.txt
    _contribution_meta.yaml
```

Each sidecar payload mirrors the real Pydantic schema, plus a `_contribution:` wrapper block (see skill specs). Maintainers run a one-shot upsert script post-review that strips `_contribution:` and merges the payload into `knowledge_base/hosted/content/`. The two-reviewer clinical signoff gate (CHARTER §6.1) fires at the upsert step, not at PR merge into `main`.

This isolation buys three things:

1. Pre-commit Pydantic validation runs against `_contribution`-wrapped sidecars without choking on the wrapper (validation runs only on `knowledge_base/hosted/content/`).
2. Contributors can submit drafts that fail clinical signoff without polluting the hot path.
3. Multi-contributor parallel work cannot collide on the same hosted YAML — collisions are confined to the contributor's own chunk directory.

## Where computation happens

| Phase | Where | What runs |
|---|---|---|
| Drafting / generation | Contributor's machine, contributor's AI tool (Codex, Claude Code, Cursor, ChatGPT) | LLM-essential work — semantic reading, synthesis, judgment, evidence drafting |
| Pre-submission self-check | Contributor's machine | Optional — contributor can re-run schema validation locally before opening PR |
| Submission | GitHub PR | Sidecar files committed; `_contribution.ai_tool` + `ai_model` recorded |
| Mechanical re-verification | Maintainer-run script (or CI bot) | Schema, source-resolution, manifest-scope, banned-source, no-OncoKB, ai_tool/model presence |
| Computational re-verification | Maintainer-run script | Where applicable, independently re-execute the mechanical part of the task and diff against contributor output (see per-chunk spec) |
| Sample human re-verification | Maintainer or Clinical Co-Lead | Spot-check N% of rows / entities by reading the actual source — per-chunk threshold |
| Clinical signoff (claim-bearing only) | 2 of 3 Clinical Co-Leads | Triggered at the maintainer-run upsert step, not at PR merge |

The contributor's machine + tools are **opaque** to the maintainer. Every check above runs against the **PR output** — sidecar files, manifest, metadata. The contributor's prompts, sessions, retries are not auditable. This is by design: chunks must produce outputs that are recoverable from the artifacts alone, without trusting the contributor's process.

## Re-verification framework

Every chunk spec must declare:

1. **Pre-acceptance gates** — mechanical checks that auto-reject before maintainer time is spent.
2. **Computational re-verify** — where applicable, an independent re-execution of the mechanical part to compare against contributor output.
3. **Sample re-verify** — what fraction of output rows the maintainer / Co-Lead reads by hand.
4. **Trust threshold** — agreement rate above which the batch is accepted, below which it is rejected wholesale.

Verification spec lives in each chunk's spec file. See `chunks/openonco/<chunk-id>.md` for per-chunk verification details.

## File-set partitioning (no two active chunks touch the same entity)

OpenOnco's CLAUDE.md flags two agents writing the same file as a coordination bug. The chunk-shelf design must guarantee that no two **active** chunks target the same `BMA-*` / `BIO-*` / `DRUG-*` / `IND-*` / `SRC-*` ID at the same time.

Each chunk receives a `task_manifest.txt` listing the explicit entity IDs (or filename ranges) it owns. The maintainer who opens a chunk-task issue checks the new manifest against currently-open manifests; overlap blocks the open.

Outputs targeting entities outside the chunk's own manifest are auto-rejected.

## Source allowlist

The pilot uses these sources only:

| Source | License | Notes |
|---|---|---|
| **CIViC** | CC0 | Primary actionability source post-2026-04-27 pivot. `SRC-CIVIC` for top-level citations; `SRC-CIVIC-EID-<n>` for specific Evidence Items. |
| **ClinicalTrials.gov** | Public domain | Trial protocols and registered outcomes. |
| **PubMed (abstracts)** | NLM terms | Abstract-only support is acceptable when chunk authorizes; mark abstracts vs. full-text in `rationale`. |
| **PubMed Central OA subset** | varies (each article) | Full-text OK only for Open Access subset. |
| **DailyMed** | Public domain | FDA-curated drug labels. |
| **openFDA** | Public domain | Drug approval, AE, recall data. |
| **ESMO open guidelines** | varies | Cite section + version. |
| **ASCO open guidelines** | varies | Same as ESMO. |
| **NCCN guidelines** | restricted redistribution | Cite by reference only — `SRC-NCCN-<DISEASE>-<VERSION>`, `source_section:`. Do not paste guideline text. |
| **WHO Classification of Tumours** | restricted | Cite by reference only. |
| **МОЗ України** orders | public | Ukrainian Ministry of Health protocols. `precedence_policy: national_floor_only`. |

Banned sources for the pilot:

- **OncoKB** — ToS conflicts with CHARTER §2 (free public, non-commercial).
- **SNOMED CT** — license-gated.
- **MedDRA** — license-gated.

## Citation format

Every clinical claim cites a `Source` (`SRC-*`) entity by stable ID, not a free URL.

- BMA / Biomarker / Drug `sources:` and `primary_sources:` fields hold lists of `SRC-*` IDs.
- Indication `sources:` holds a list of `Citation` objects: `{id: SRC-*, section: "..."}` or `{id: SRC-*, evidence_id: "EID12345"}`.
- BMA `evidence_sources:` holds `EvidenceSourceRef` entries with `source: SRC-*`, `level: <source-native token>`, `evidence_ids: [...]`, optional `direction` and `significance`.

If the source needs ingestion, file a `source_stub.yaml` under `contributions/<chunk-id>/`.

## Reviewer routing

| Chunk topic | Maintainer review | Clinical Co-Lead signoff (CHARTER §6.1) |
|---|---|---|
| Citation verification (report only) | 1 maintainer | Not required — reports do not edit hosted content. |
| Biomarker reconstruction / extraction | 1 maintainer | 2 of 3 Clinical Co-Leads at upsert time. |
| Drug / Indication evidence drafting | 1 maintainer | 2 of 3 Clinical Co-Leads at upsert time. |
| Recommendation-wording audit | 1 maintainer | Not required — report only. |
| UA translation review | 1 maintainer | 1 Ukrainian-fluent clinician at upsert. |
| Source-stub ingest | 1 maintainer | Not required for stub itself. |

Sidecar PRs merge to `main` after one maintainer review. The clinical signoff gate fires at the maintainer-run upsert step.

## AI tool + model metadata (required, non-blocking on accept/reject)

Every sidecar's `_contribution` wrapper carries:

- `ai_tool` — short tool name. Required.
- `ai_model` — short model identifier. Required.
- `ai_model_version` — optional snapshot/build/checkpoint string.
- `ai_session_notes` — optional free-form generation-method notes.

**Why required:** model metadata is the audit signal that makes external computation recoverable. If a regression class is later attributed to a specific model, maintainers can re-verify affected sidecars by metadata sweep.

**Why non-blocking on content:** verification gates check the **output**, not the **input**. Acceptance must not be conditioned on model — that would create the wrong incentive (clinicians shortcutting review for "trusted" models). Missing metadata triggers auto-reject for completeness, but model identity itself never blocks merge.

**Privacy:** do not include raw prompts, API keys, account identifiers, or proprietary system-prompt content in `ai_session_notes`.

## Machine-checkable acceptance criteria

A chunk PR is auto-rejected if any of these fail:

- Any sidecar is missing `_contribution.ai_tool` or `_contribution.ai_model`.
- `pytest tests/` does not pass on the contributor branch.
- Pydantic validation rejects any sidecar payload (after `_contribution:` strip).
- `git diff --name-only main..HEAD` lists any file outside `contributions/<chunk-id>/`.
- `task_manifest.txt` is missing or contains entity IDs not in the chunk-task issue's manifest.
- Any `_contribution.target_action: upsert` references a `target_entity_id` that does not exist on `main`.
- Any `_contribution.target_action: new` collides with an existing entity ID on `main`.
- Any `evidence_sources[*].source` or `primary_sources` entry references a `SRC-*` ID that does not exist on `main` AND no corresponding `source_stub_<id>.yaml` is in the chunk directory.
- Any `evidence_sources[*].source: SRC-ONCOKB` appears in a contributor-authored sidecar.

## Existing OpenOnco repo conventions to follow

- Branch naming: `tasktorrent/<chunk-id>`.
- Never commit to `master` / `main` directly.
- No `git add -A` / `git add .` — explicit pathspecs only.
- No `--no-verify`. Pre-commit hooks always run.

## Ukrainian-language fields

OpenOnco specs are in Ukrainian and stay Ukrainian. Many entities have `*_ua` companion fields. Pilot policy:

- BMA / drug / citation chunks may submit English-only payloads. Set `ukrainian_review_status: pending_translation` where the field exists.
- Disease-page chunks must preserve existing UA fields verbatim and flag any new claim with `ukrainian_review_status: pending_translation`.
- Do not machine-translate UA fields and submit them as `complete`.

## What contributors should not do

- Edit any file under `knowledge_base/hosted/content/`, `specs/`, `docs/`, or `legacy/`.
- Submit a sidecar that depends on a non-existent `SRC-*` without a `source_stub.yaml`.
- Bundle multiple chunks in one PR.
- Rewrite clinical claim text as `support_status: supported` from a memory-based judgment.

## What maintainers commit to

- A response on every chunk PR within 7 working days.
- A single rejection comment template per failure mode.
- Active chunk count capped at 10 during the pilot.

## Pilot success criteria

The pilot is "successful enough to expand" if, across the first wave of chunks:

- Both PRs pass machine-checkable gates after at most 1 cycle of feedback.
- Computational re-verify (where applicable) shows ≥ 95% agreement with contributor output.
- Sample human re-verify shows ≥ 90% agreement on row-level judgments.
- No clinical-content drift slips into `main` without two-Clinical-Co-Lead signoff.
- Maintainer review burden per chunk averages under 4 hours.

If those numbers don't hold, fix the chunk specs before opening a second wave.
