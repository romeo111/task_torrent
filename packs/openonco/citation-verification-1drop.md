# OpenOnco Drop Pack: Citation Verification

## Pack ID

`openonco-citation-verification-1drop`

## Status

**Pilot Pack 2 candidate.** Opens after `openonco-civic-bma-reconstruction-1drop` (Pack 1) closes successfully. The seed corpus is the OpenOnco audit report `docs/reviews/citation-verification-2026-04-27.md` — 914 findings across 464 entities — partitioned into chunks by source domain to avoid two contributors checking the same `(entity, claim, source)` triple.

## Mission

Verify whether each `(entity, claim, source)` triple listed in the chunk manifest is supported by the cited source. Output is a per-chunk `citation-report.yaml` (sidecar, no edits to hosted content) that maintainers act on.

## Total

1 Drop

## Required Skills

- Citation verification

## Allowed Sources

See `docs/openonco-pilot-workflow.md` §"Source allowlist". The chunk manifest specifies which source domain each chunk owns; do not check rows from outside that domain.

## Output Format

Sidecar report at `contributions/openonco-citation-verification-1drop/<chunk-id>/citation-report.yaml`. Schema in `skills/citation-verification.md`. New `Source` proposals (when `suggested_action: source_stub_needed`) go in the same chunk directory as `source_stub_<proposed_id>.yaml`.

## Chunks

Partitioned by source domain so no two chunks check the same row. The chunk manifest seed comes from `docs/reviews/citation-verification-2026-04-27.md` filtered by source `SRC-*` prefix.

| Chunk ID | Source domain | Drop Estimate | Manifest source |
| --- | --- | ---: | --- |
| `openonco-citation-verification-c1` | PubMed / PMC entries | 0.20 | All rows from the audit where `source_id` starts `SRC-PMID-` or `SRC-PMC-` |
| `openonco-citation-verification-c2` | CIViC entries | 0.15 | All rows where `source_id` is `SRC-CIVIC` or `SRC-CIVIC-EID-*` |
| `openonco-citation-verification-c3` | NCCN-by-reference | 0.20 | All rows where `source_id` starts `SRC-NCCN-` |
| `openonco-citation-verification-c4` | DailyMed / openFDA / FDA labels | 0.15 | All rows where `source_id` starts `SRC-DAILYMED-`, `SRC-OPENFDA-`, or `SRC-FDA-LABEL-` |
| `openonco-citation-verification-c5` | ESMO / ASCO / WHO / МОЗ + wrap-up summary report | 0.30 | All remaining rows + cross-chunk duplicate-row sweep |

Each chunk's `chunk_manifest.txt` lists explicit `(entity_id, claim_locator, source_id)` triples. Manifests across chunks are disjoint. PRs targeting rows outside the manifest are auto-rejected.

## Acceptance Criteria

- Every row in the chunk manifest has exactly one corresponding row in `citation-report.yaml`.
- Every row has `support_status`, `rationale` (≥ 1 sentence with locator), `accessed:` date, and `suggested_action`.
- `support_status: supported` rows quote or precisely cite the source section that attests the claim.
- `support_status: broken_link` rows distinguish "URL does not resolve" from "Source.superseded_by points to missing entity".
- For `suggested_action: replace_source`, the `suggested_replacement_source_id` is an existing `SRC-*` ID (verified to exist on `main`).
- For `suggested_action: source_stub_needed`, a corresponding `source_stub_*.yaml` exists in the same chunk directory.
- No edits to `knowledge_base/hosted/content/` — sidecar report only.

## Rejection Criteria

- Row marked `supported` without a section/page locator or quote in `rationale`.
- Replacement source is a URL or an invented `SRC-*` ID.
- Claim text rewritten inside `rationale` instead of described.
- Topic-adjacent source treated as direct support.
- PR touches files outside `contributions/openonco-citation-verification-1drop/<chunk-id>/`.
- Banned source (e.g. `SRC-ONCOKB`) flagged as `supported` instead of `access_blocked`.

## Reviewer

- Maintainer review (1) at PR merge.
- No Clinical Co-Lead signoff required for the report itself — the report does not edit hosted content. Subsequent maintainer-driven edits to hosted content (acting on the report's findings) follow the standard CHARTER §6.1 two-reviewer flow.

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Do not invent replacement citations
- Do not rewrite clinical claims as supported without source evidence
- Maintainer review required before any hosted-content change
