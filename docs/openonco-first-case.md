# OpenOnco First Case

## Pilot Role

OpenOnco is the first pilot case for TaskTorrent. It is useful because it has structured knowledge needs, citation-sensitive content, and clear maintainer review requirements.

The TaskTorrent model must remain general. OpenOnco should test the pack and review workflow, not define the limits of the platform.

## Pilot operational doc

The day-to-day rules for OpenOnco contributors and maintainers — sidecar workflow, source allowlist, reviewer routing, partitioning rules, machine-checkable acceptance criteria — live in [`docs/openonco-pilot-workflow.md`](./openonco-pilot-workflow.md). That document is the source of truth when this one and it disagree.

## Initial Pack Plan

Sequential, not parallel. Pack 2 does not open until Pack 1's chunks are reviewed and either merged or rejected.

| Order | Pack | Why first | Status |
|---|---|---|---|
| 1 | [`openonco-civic-bma-reconstruction-1drop`](../packs/openonco/civic-bma-reconstruction-1drop.md) | Acute need post-CIViC pivot (399 BMA files flagged `actionability_review_required: true`); deterministic acceptance criteria. | Ready to open. |
| 2 | [`openonco-citation-verification-1drop`](../packs/openonco/citation-verification-1drop.md) | Seed corpus exists (audit report with 914 findings); sidecar-report-only output is low risk. | Ready after Pack 1 closes. |
| 3 | [`openonco-pancreatic-biomarkers-1drop`](../packs/openonco/pancreatic-biomarkers-1drop.md) | Documented coverage gap; tests the new-BMA-from-evidence drafting flow. | Ready after Pack 2 closes. |
| 4 (later) | [`openonco-lung-egfr-evidence-1drop`](../packs/openonco/lung-egfr-evidence-1drop.md) | Lower priority; EGFR/lung is well-covered already. | Hold until pilot ramps. |

## Default Demand Queue

If a contributor has no topic preference, route them to the OpenOnco demand queue.

The initial demand queue should prioritize:

- Citation verification for existing content
- High-impact biomarker coverage gaps
- Normalization work that reduces reviewer burden
- Disease pages with clear maintainer-provided scope
- Dataset cleanup that has deterministic acceptance criteria

## Safety Boundary

OpenOnco work must not provide medical advice, treatment recommendations, or patient-specific outputs. Contributors should map evidence, verify citations, normalize data, and prepare reviewable drafts.

Every clinical claim must include source links via `SRC-*` stable IDs (not raw URLs). Every AI-generated output must be reviewed by maintainers before publication. Claim-bearing changes that touch `knowledge_base/hosted/content/` need 2 of 3 Clinical Co-Lead signoffs (CHARTER §6.1) at the maintainer-run upsert step — sidecar PRs do not pass that gate by themselves.

## Maintainer Q&A — concrete pilot answers

These were the open questions in the original draft of this file. Concrete answers, with pointers to the operational doc:

| Q | Pilot answer |
|---|---|
| What schema do biomarker outputs target first? | `BiomarkerActionability` (BMA), schema `knowledge_base/schemas/biomarker_actionability.py`. Pack 1 reconstructs `evidence_sources` blocks for ~399 flagged BMA files. |
| Edit existing files or sidecar? | **Sidecar.** All contributor output lands under `contributions/<pack-id>/<chunk-id>/`. Maintainers run an upsert script post-review. See `docs/openonco-pilot-workflow.md` §"Sidecar workflow". |
| Source types allowed? | CIViC (CC0), ClinicalTrials.gov, PubMed (abstracts + PMC OA), DailyMed, openFDA, ESMO/ASCO open guidelines, NCCN-by-reference, WHO-by-reference, МОЗ України. **Banned:** OncoKB, SNOMED CT, MedDRA. Full table in `docs/openonco-pilot-workflow.md` §"Source allowlist". |
| Citation format? | Reference `Source` (`SRC-*`) entities by stable ID. New sources need a `source_stub.yaml` filed alongside the chunk's other outputs; maintainers ingest them through `specs/SOURCE_INGESTION_SPEC.md` §8/§20. |
| Highest-priority disease/biomarker areas? | (a) ~399 BMA files post-CIViC pivot (Pack 1 takes the NSCLC subset); (b) 914 audit findings in `docs/reviews/citation-verification-2026-04-27.md` (Pack 2); (c) pancreatic biomarker gap (Pack 3). NSCLC, breast, CRC, melanoma, GIST, AML have the strongest CIViC + OpenOnco overlap. |
| Reviewer routing? | Citation reports + dataset normalization → 1 maintainer. BMA / Drug / Indication / claim-bearing disease pages → 1 maintainer at PR + 2 of 3 Clinical Co-Leads at upsert. Table in `docs/openonco-pilot-workflow.md` §"Reviewer routing". |
| Minimum reviewable fields? | Per skill spec: `_contribution.{pack_id, chunk_id, contributor, target_action, target_entity_id, ai_tool}` plus the schema's required fields. Plus a chunk-level `chunk_manifest.txt`. |
| Duplicate handling? | Detect by 4-tuple `(disease, biomarker, drug, alteration)` against existing entities. Mark canonical via `target_action: flag_duplicate` + `duplicate_of: <stable-id>`. Never silently drop. |
| Existing labels / branch rules / PR conventions? | Branch `tasktorrent/<pack-id>/<chunk-id>`. Never commit to `master`/`main`. Pre-commit hooks always run; no `--no-verify`. No `git add -A` / `git add .`. New issue templates `tasktorrent-{chunk-task,help-pack}.md` live alongside OpenOnco's existing `.github/ISSUE_TEMPLATE/*` rather than replacing them. |
| What helps maintainers without growing review burden? | Sidecar isolation; pre-validation CI that rejects bad PRs before maintainer touches them; standardized rejection-comment templates; one pack open at a time during the pilot. |
