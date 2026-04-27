# OpenOnco First Case

## Pilot Role

OpenOnco is the first pilot case for TaskTorrent. It has structured knowledge needs, citation-sensitive content, and clear maintainer review requirements — all properties that test the chunk-shelf workflow.

The TaskTorrent model must remain general. OpenOnco tests the workflow; it does not define the limits of the platform.

## Operational doc

Day-to-day rules — sidecar workflow, source allowlist, reviewer routing, partitioning, machine-checkable acceptance criteria, active-cap, AI-model metadata, re-verification framework — live in [`docs/openonco-pilot-workflow.md`](./openonco-pilot-workflow.md). That document is the source of truth when this one and it disagree.

## Pilot shape

- **Minimum chunk size: ~1M tokens (~10 Drops).**
- **Active chunks at any time: 2.**
- **Shelf: 7 chunks pre-drafted, ~84 Drops total work surface.**
- One chunk = one contributor = one PR = one review.

The sequencing rule (no second active chunk until first closes) is replaced by an explicit active-cap of 10 (raised from initial 2 after the first wave validated the pipeline). Up to 10 chunks may run in parallel if their manifests are disjoint.

## Chunk shelf

Defined in [`chunks/openonco/`](../chunks/openonco/). Summary:

| Chunk | Drops | Where compute happens | Re-verification profile |
|---|---:|---|---|
| `civic-bma-reconstruct-all` | ~12 | Contributor + local CIViC snapshot | 100% computational re-run + 5% Co-Lead spot-check |
| `citation-verify-914-audit` | ~10 | Contributor + web access | Schema + URL/EID checks + 10% maintainer spot-check |
| `rec-wording-audit-claim-bearing` | ~10 | Contributor (repo read-only) | Regex cross-check (0 misses) + 5% maintainer sample |
| `ua-translation-review-batch` | ~12 | Contributor (repo read-only, bilingual) | Untranslated-fragment auto-detect + 15% UA-clinician sample |
| `redflag-indication-coverage-fill` | ~15 | Contributor + web access | 100% Co-Lead read for claim-bearing cells |
| `bma-drafting-gap-diseases` | ~15 | Contributor + CIViC + web | 100% CIViC EID re-verify + 100% Co-Lead read |
| `source-stub-ingest-batch` | ~10 | Contributor + web access | URL resolution + 100% license accuracy on sample |

The first two chunks are the proposed pilot wave. Others sit in queue.

## Maintainer Q&A — concrete pilot answers

| Q | Pilot answer |
|---|---|
| What schema do biomarker outputs target? | `BiomarkerActionability` (BMA), `Biomarker` (BIO-*), `Source` (SRC-*) per `cancer-autoresearch/knowledge_base/schemas/`. |
| Edit existing files or sidecar? | **Sidecar.** All output under `contributions/<chunk-id>/`. Maintainer runs upsert script post-review. |
| Source types allowed? | CIViC, ClinicalTrials.gov, PubMed (abstract + PMC OA), DailyMed, openFDA, ESMO/ASCO open, NCCN-by-reference, WHO-by-reference, МОЗ України. **Banned:** OncoKB, SNOMED CT, MedDRA. |
| Citation format? | Reference `Source` (`SRC-*`) by stable ID. New sources need `source_stub.yaml` per `SOURCE_INGESTION_SPEC.md` §8/§20. |
| Highest priority? | (1) ~399 BMA files post-CIViC pivot, (2) 914-finding audit report, (3) coverage-gap diseases. |
| Reviewer routing? | Reports + audits → 1 maintainer. Claim-bearing into `hosted/content/` → 1 maintainer + 2 of 3 Clinical Co-Leads at upsert. |
| Minimum reviewable fields? | Per skill spec: `_contribution.{chunk_id, contributor, target_action, target_entity_id, ai_tool, ai_model}` plus the schema's required fields plus a chunk-level `task_manifest.txt`. |
| Duplicate handling? | Detect by 4-tuple `(disease, biomarker, drug, alteration)`. Mark canonical via `target_action: flag_duplicate` + `duplicate_of: <stable-id>`. Never silently drop. |
| Existing labels / branch rules / PR conventions? | Branch `tasktorrent/<chunk-id>`. Never commit to `master`/`main`. Pre-commit hooks always run; no `--no-verify`. No `git add -A`/`git add .`. |
| What helps maintainers without growing review burden? | Sidecar isolation + computational re-verification + sample-based human re-verify + active-cap (currently 10). |

## Why "Pack" no longer appears

Earlier drafts of TaskTorrent had Packs grouping ~5 chunks each. That layer added ceremony without proportional value: chunks already have stable IDs, manifests, and labels; "pack" was a redundant grouping primitive. Topic grouping is now done via GitHub labels.

## Re-verification policy

Every chunk spec declares:

1. **Pre-acceptance gates** — auto-reject mechanical
2. **Computational re-verify** — independent re-execution of the mechanical part where applicable
3. **Sample human re-verify** — N% spot-check threshold
4. **Trust threshold** — agreement rate above which the batch is accepted

The contributor's machine + tool are opaque. All checks run against the PR output, not the contributor's process. AI-tool + AI-model metadata is captured in `_contribution` for audit/regression-triage but does not gate accept/reject — verification is output-based, not input-based.
