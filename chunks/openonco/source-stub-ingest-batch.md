# Chunk: source-stub-ingest-batch

## Status

`queued`

## Topic Labels

`source-ingest`, `metadata-only`

## Mission

For known source-ingest TODOs (14 listed in `cancer-autoresearch/docs/reviews/bma-coverage-2026-04-27.md` plus audit-driven gaps), draft `Source` (`SRC-*`) stub YAMLs with full licensing classification per `specs/SOURCE_INGESTION_SPEC.md`. Output: per-source stubs that maintainers ingest through the existing source-review flow.

This chunk does NOT promote sources to hosted content — that's a separate maintainer-driven path with H1–H5 hosting justification. Output is stub drafts only.

## Drop Estimate

~10 Drops (~1.0M tokens). ~30–50 source candidates × ~25k tokens per stub (read source page, extract metadata, classify license, fill SOURCE_INGESTION_SPEC fields, write attribution + restrictions block).

## Required Skill

`citation-verification` (for source resolution + licensing reading) plus careful adherence to `specs/SOURCE_INGESTION_SPEC.md`.

## Allowed Sources

The sources to be stubbed must each be on the pilot allowlist. The chunk does NOT introduce new banned-source stubs — if a TODO points at OncoKB or SNOMED, it's marked `cannot_ingest_per_pilot_allowlist` instead.

## Manifest

The maintainer commits the canonical list of source candidates with their identifying URL/DOI/citation. Each candidate falls into:

- `pubmed_open_access` — PMC OA articles needed for evidence support
- `civic_eid_specific` — particular `SRC-CIVIC-EID-<n>` for high-traffic claims
- `nccn_version` — NCCN version pins (e.g. `SRC-NCCN-PDAC-2025-V2`)
- `esmo_guideline` — ESMO open guidelines
- `dailymed_drug` — DailyMed entries for drugs cited but not yet stubbed
- `clinicaltrials_protocol` — specific CT.gov registrations cited

## Computation

For each candidate:

1. **Resolve** the URL / DOI / NCT ID / EID.
2. **Fetch** the source page or metadata.
3. **Read** licensing / terms-of-use / copyright statement.
4. **Classify**:
   - `license.spdx_id` — SPDX identifier where one exists; otherwise verbatim license text in `license.text`.
   - `commercial_use_allowed`, `redistribution_allowed`, `modifications_allowed`, `sharealike_required` — booleans from license terms.
   - `hosting_mode` — almost always `referenced` for the pilot. Hosting requires explicit H1–H5 justification per SOURCE_INGESTION_SPEC §1.4 — do not propose hosting in this chunk.
   - `attribution.required` and `attribution.text` — verbatim attribution string per source's terms.
5. **Fill metadata** — `source_type`, `title`, `authors`, `journal`, `version`, `current_as_of`, `evidence_tier` per `specs/CLINICAL_CONTENT_STANDARDS.md` tier table.
6. **Build `precedence_policy`** — see SOURCE_INGESTION_SPEC §3 (`leading` for NCCN/ESMO/ASCO Tier-1, `secondary_evidence_base` for CIViC, `national_floor_only` for МОЗ).
7. **Pages / references count** — round to nearest 50 references / 10 pages. Don't claim more precision than you have.
8. **Write stub** at `contributions/source-stub-ingest-batch/source_stub_<src_id>.yaml` with `_contribution.target_action: new`.

## Where computation happens

Contributor's machine. Required:

- Web access (PubMed, CIViC, NCCN landing pages, ESMO/ASCO publication pages, DailyMed, ClinicalTrials.gov).
- Read access to `cancer-autoresearch/specs/SOURCE_INGESTION_SPEC.md` and `specs/CLINICAL_CONTENT_STANDARDS.md`.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on every stub (matches `knowledge_base/schemas/source.py`).
- Every `id` is genuinely new (no collision on `main`).
- `license` block is non-empty (either `spdx_id` or verbatim `text`).
- `commercial_use_allowed`, `redistribution_allowed`, `modifications_allowed`, `sharealike_required` are all explicitly set (no nulls).
- `hosting_mode: referenced` (no contributor-proposed hosting).
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify

Maintainer runs:

- HTTP HEAD on `Source.url` for every stub. 4xx/5xx → reject row.
- For PubMed entries: confirm `pmid` resolves to a valid record via NLM API.
- For CIViC EIDs: confirm the EID exists in the local CIViC snapshot.

### Sample human re-verify (20%)

Maintainer reads ~10 random stubs:

- License classification matches the source's stated license.
- `precedence_policy` is appropriate.
- Attribution string is verbatim from source.
- Evidence tier matches `CLINICAL_CONTENT_STANDARDS.md`.

### Trust threshold

- Gates: 100%.
- Computational re-verify: 100%.
- License accuracy in sample: 100% (license errors are blocking — wrong classification could violate terms).

## Output Format

`contributions/source-stub-ingest-batch/source_stub_<src_id>.yaml` per source. Plus `task_manifest.txt`, `_contribution_meta.yaml`.

## Acceptance Criteria

- All gates pass.
- 100% URL resolution.
- 100% license accuracy on sample.

## Rejection Criteria

- Wrong license classification (treats restricted source as open).
- Hosting proposed by contributor.
- Source on banned-source list.
- Missing attribution where source requires it.
- Stub references `id` that already exists on `main`.

## Claim Method

`trusted-agent-wip-branch-first` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1.
- No Clinical Co-Lead signoff for stubs themselves. Full Source promotion follows `specs/SOURCE_INGESTION_SPEC.md` §8 + §20 separately.

## Notes

License classification is high-stakes. A stub mislabeled as "redistribution_allowed: true" for a restricted source could lead OpenOnco to violate the source's terms. The 100% license-accuracy threshold reflects that.
