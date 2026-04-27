# OpenOnco Pilot Workflow

This document is the operational layer between TaskTorrent's general pack/chunk model and OpenOnco's actual repo conventions. It exists because OpenOnco has stricter clinical-content review rules than the generic TaskTorrent pilot assumes (CHARTER §6.1 two-reviewer signoff for `knowledge_base/hosted/content/`, pre-commit Pydantic validation, multi-agent coordination protocol). This doc names the rules so contributors don't trip them.

If anything here conflicts with the OpenOnco repo's `CLAUDE.md`, `specs/CHARTER.md`, or `specs/SOURCE_INGESTION_SPEC.md`, the OpenOnco source-of-truth wins.

## Sidecar workflow (do not edit hosted content directly)

Contributor PRs **do not** edit files under `knowledge_base/hosted/content/`. They write **sidecar files** under a new top-level `contributions/` tree:

```
contributions/
  <pack-id>/
    <chunk-id>/
      bma_<biomarker>_<variant>_<disease>.yaml
      bio_<biomarker>.yaml
      drug_<drug>.yaml
      ind_<indication>.yaml
      source_stub_<src_id>.yaml
      citation-report.yaml
      chunk_manifest.txt
      _contribution_meta.yaml
```

Each sidecar file's payload mirrors the real Pydantic schema, plus a `_contribution:` wrapper block (see skill specs). Maintainers run a one-shot upsert script post-review that strips `_contribution:` and merges the payload into `knowledge_base/hosted/content/`. The two-reviewer clinical signoff gate (CHARTER §6.1) fires at the upsert step, not at PR merge into `main`.

This isolation buys three things:

1. Pre-commit Pydantic validation runs against `_contribution`-wrapped sidecars without choking on the wrapper, because validation only runs on `knowledge_base/hosted/content/`.
2. Contributors can submit drafts that fail clinical signoff without polluting the hot path.
3. Multi-agent / multi-contributor parallel work cannot collide on the same hosted YAML file — collisions are confined to the contributor's own chunk directory.

## File-set partitioning (no two chunks touch the same entity)

OpenOnco's CLAUDE.md flags two agents writing the same file as a coordination bug. The pack design must guarantee that no two chunks across active packs target the same `BMA-*` / `BIO-*` / `DRUG-*` / `IND-*` / `SRC-*` ID.

Partition rule for each pack: each chunk receives a `chunk_manifest.txt` listing the explicit entity IDs (or filename ranges) it owns. Manifests across chunks within a pack must be disjoint. Manifests across active packs must also be disjoint — the maintainer who opens a pack is responsible for checking against currently-open chunk manifests.

Outputs targeting entities outside the chunk manifest are auto-rejected.

## Source allowlist

The pilot uses these sources only:

| Source | License | Notes |
|---|---|---|
| **CIViC** | CC0 | Primary actionability source post-2026-04-27 pivot. `SRC-CIVIC` for top-level citations; `SRC-CIVIC-EID-<n>` for specific Evidence Items. |
| **ClinicalTrials.gov** | Public domain | Trial protocols and registered outcomes. |
| **PubMed (abstracts)** | NLM terms | Abstract-only support is acceptable when chunk authorizes; mark abstracts vs. full-text in `rationale`. |
| **PubMed Central OA subset** | varies (each article) | Full-text OK only for Open Access subset. Confirm OA license in source stub. |
| **DailyMed** | Public domain | FDA-curated drug labels. |
| **openFDA** | Public domain | Drug approval, AE, recall data. |
| **ESMO open guidelines** | varies | Cite section + version. Some are open-access PDFs; abstracts/summaries always allowed. |
| **ASCO open guidelines** | varies | Same as ESMO. |
| **NCCN guidelines** | restricted redistribution | Cite by reference only — `SRC-NCCN-<DISEASE>-<VERSION>`, `source_section:` for the page/section. Do not paste guideline text into the repo. |
| **WHO Classification of Tumours** | restricted | Cite by reference only. |
| **МОЗ України** orders | public | Ukrainian Ministry of Health protocols. `precedence_policy: national_floor_only`. |

Banned sources for the pilot:

- **OncoKB** — ToS conflicts with CHARTER §2 (free public, non-commercial). See `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` in the OpenOnco repo. Pre-existing `SRC-ONCOKB` entries are legacy migration metadata; the render layer skips them.
- **SNOMED CT** — license-gated.
- **MedDRA** — license-gated.

Conditional:

- Paywalled full-text journal articles — abstract-only support is acceptable when the chunk explicitly authorizes it; flag `support_status: unclear` when abstract is insufficient. Do not file a `source_stub.yaml` for paywalled-only sources without maintainer instruction.

## Citation format

Every clinical claim cites a `Source` (`SRC-*`) entity by stable ID, not a free URL.

- BMA / Biomarker / Drug `sources:` and `primary_sources:` fields hold lists of `SRC-*` IDs.
- Indication `sources:` holds a list of `Citation` objects: `{id: SRC-*, section: "..."}` or `{id: SRC-*, evidence_id: "EID12345"}`.
- BMA `evidence_sources:` holds `EvidenceSourceRef` entries with `source: SRC-*`, `level: <source-native token>`, `evidence_ids: [...]`, optional `direction` and `significance`.

If the source you need has no `SRC-*` entity yet, file a `source_stub.yaml` under `contributions/<pack-id>/<chunk-id>/`. Maintainers ingest stubs through `specs/SOURCE_INGESTION_SPEC.md` §8 + §20, including license classification and H1–H5 hosting justification when the stub proposes hosting.

## Reviewer routing

| Pack category | Maintainer review | Clinical Co-Lead signoff (CHARTER §6.1) |
|---|---|---|
| Citation verification (report only) | 1 maintainer | Not required — reports do not edit hosted content. |
| Biomarker extraction (BIO-* / BMA-* sidecars) | 1 maintainer | 2 of 3 Clinical Co-Leads at upsert time. |
| Drug evidence mapping (DRUG-* / IND-* sidecars) | 1 maintainer | 2 of 3 Clinical Co-Leads at upsert time. |
| Disease page improvement | 1 maintainer | 2 of 3 Clinical Co-Leads if claim-bearing. |
| Dataset normalization | 1 maintainer | Not required if no claim semantics change. |

Sidecar PRs merge to `main` after one maintainer review. The clinical signoff gate fires at the upsert step that merges sidecars into `knowledge_base/hosted/content/` — that step is run by maintainers, not contributors.

## Machine-checkable acceptance criteria

A chunk PR is auto-rejected if any of these fail:

- `pytest tests/` does not pass on the contributor branch.
- `python -m knowledge_base.validation.validate` rejects any sidecar payload (after the maintainer-run script strips `_contribution:`).
- `git diff --name-only main..HEAD` lists any file outside `contributions/<pack-id>/<chunk-id>/`.
- `chunk_manifest.txt` is missing or contains entity IDs not in the chunk's allowlist.
- Any `_contribution.target_action: upsert` references a `target_entity_id` that does not exist on `main`.
- Any `_contribution.target_action: new` collides with an existing entity ID on `main`.
- Any `evidence_sources[*].source` or `primary_sources` entry references a `SRC-*` ID that does not exist on `main` AND no corresponding `source_stub_<id>.yaml` is in the same chunk directory.
- Any `evidence_sources[*].source: SRC-ONCOKB` appears in a contributor-authored sidecar (legacy entries are exempt; pilot output is not).

A maintainer-side bot or workflow runs these checks and posts a single comment with pass/fail per check. Contributors fix and force-push to their PR branch.

## Existing OpenOnco repo conventions to follow

- Branch naming: `tasktorrent/<pack-id>/<chunk-id>` (greppable, sortable).
- Never commit to `master` / `main` directly. Always work on a branch.
- No `git add -A` or `git add .` — explicit pathspecs only. Multi-agent runs leave untracked files; `-A` swallows them.
- No `--no-verify`. Pre-commit hooks always run.
- Pre-existing issue templates (`.github/ISSUE_TEMPLATE/{new_cancer_type, report_correction, research_request}.md`) and PR template stay as-is. The TaskTorrent pilot adds `tasktorrent-chunk-task.md` and `tasktorrent-help-pack.md` alongside, not replacing.

## Ukrainian-language fields

OpenOnco specs are in Ukrainian and stay Ukrainian. Many entities have `*_ua` companion fields (`evidence_summary_ua`, `names.uk`, etc.) and a `ukrainian_review_status` flag. Pilot policy:

- Biomarker / drug / citation packs may submit English-only payloads. Set `ukrainian_review_status: pending_translation` where the field exists.
- Disease-page-improvement packs (when added) must preserve existing UA fields verbatim and flag any new claim with `ukrainian_review_status: pending_translation` for maintainer-side translation review.
- Do not machine-translate UA fields and submit them as `ukrainian_review_status: complete`. Translation requires clinical review (CLAUDE.md, `specs/CLINICAL_CONTENT_STANDARDS.md`).

## What contributors should not do

- Edit any file under `knowledge_base/hosted/content/`.
- Edit any file under `specs/`, `docs/`, or `legacy/`.
- Add new entries to existing files in any branch other than their chunk directory.
- Submit a sidecar that depends on a Source (`SRC-*`) that doesn't exist without also submitting a `source_stub.yaml` in the same chunk.
- Bundle multiple chunks in one PR. One chunk = one PR.
- Rewrite clinical claim text as `support_status: supported` from a memory-based judgment.

## What maintainers commit to

- A response on every chunk PR within 5 working days.
- A single rejection comment template per failure mode (see `docs/openonco-rejection-templates.md` — to be added in pilot Phase 1).
- One pack open at a time during the pilot. Pack 2 does not open until Pack 1's chunks are reviewed and either merged or rejected.

## Pilot success criteria

The pilot is "successful enough to expand" if, across the first pack:

- ≥ 50% of submitted chunks pass machine-checkable acceptance criteria on first submission.
- ≥ 30% of submitted chunks reach maintainer review and either merge or get a clear rejection (not blocked-on-tooling).
- No clinical-content drift slips into `main` without two-Clinical-Co-Lead signoff.
- Maintainer review burden per chunk averages under 30 minutes.

If those numbers don't hold, fix the pack/skill specs before opening Pack 2.
