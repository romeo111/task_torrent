# KB Data Quality Plan - 2026-04-29

## Purpose

This plan defines how TaskTorrent should help improve knowledge-base data quality
without letting AI-generated output bypass maintainer review.

The first target is OpenOnco, but the plan is written so another consumer repo
can reuse the same quality loop: measure, partition, chunk, verify, merge, and
track drift over time.

## Scope

In scope:

- biomarker actionability records
- biomarker, drug, indication, and source entities
- citation links and evidence IDs
- Ukrainian companion fields
- source-stub metadata
- recommendation wording and safety red flags
- schema conformance and cross-file consistency

Out of scope:

- patient-specific advice
- treatment recommendations
- direct edits to hosted clinical content by contributors
- use of banned or license-gated sources
- autonomous publication without maintainer review

## Quality Dimensions

Every KB quality task should map to one or more dimensions:

| Dimension | Question | Example failure |
|---|---|---|
| Schema validity | Does the file satisfy the consumer schema? | Missing required field or invalid enum. |
| Citation integrity | Does every clinical claim cite an allowed source? | `SRC-*` missing, stale, or unsupported by cited text. |
| Source policy | Are all sources allowed for this consumer? | OncoKB, SNOMED CT, MedDRA, or unlicensed guideline text. |
| Entity consistency | Do IDs, names, and relations agree across files? | Drug alias mismatch or duplicate biomarker actionability row. |
| Clinical reviewability | Can a maintainer verify the claim quickly? | Rationale too vague or section reference missing. |
| Localization quality | Are Ukrainian fields present, preserved, and reviewable? | Machine-translated claim marked as complete. |
| Coverage | Are expected diseases, lines of therapy, biomarkers, or sources missing? | Known high-priority disease has no BMA coverage. |
| Drift | Did an old record become stale relative to newer sources? | Outdated trial status or superseded citation. |

## OpenOnco First Work

OpenOnco is the first KB data-quality consumer because it already has the
properties TaskTorrent needs to test:

- structured YAML entities
- explicit schemas
- clinical-content safety boundaries
- citation-sensitive claims
- Ukrainian localization needs
- maintainer and Clinical Co-Lead review gates
- a sidecar workflow that isolates contributor output

Initial OpenOnco work should focus on quality tasks that are large enough to
benefit from AI-assisted review but bounded enough to be merged safely:

1. Citation verification for existing claim-bearing records.
2. CIViC Evidence Item recheck for biomarker actionability records.
3. Source-stub completeness and license classification.
4. Ukrainian translation review for visible patient-facing fields.
5. Duplicate and near-duplicate BMA detection.
6. Coverage-gap reports for diseases, biomarkers, and lines of therapy.
7. Recommendation wording audits for unsupported or overstrong claims.

## Workflow

1. **Measure.** Run schema checks, source checks, duplicate checks, and coverage
   reports against the consumer KB.
2. **Classify.** Assign each issue to a quality dimension and risk level.
3. **Partition.** Split the issue set into non-overlapping manifests.
4. **Chunk.** Write TaskTorrent chunk specs for work that needs semantic AI
   judgment or evidence reading.
5. **Claim.** Open active chunk issues only up to the consumer review cap.
6. **Submit.** Contributors write sidecar output under `contributions/<chunk-id>/`.
7. **Verify.** Maintainers run mechanical checks, computational re-verification
   where possible, and human spot checks.
8. **Integrate.** Maintainers upsert accepted sidecars into hosted content after
   required signoff.
9. **Track.** Record accepted, rejected, stale, duplicate, and deferred issues.

## Risk Levels

| Level | Meaning | Review expectation |
|---|---|---|
| Low | Mechanical metadata or report-only output. | One maintainer review. |
| Medium | Structured entity draft without direct clinical recommendation. | One maintainer review plus sampled semantic check. |
| High | Claim-bearing clinical content or visible patient-facing text. | Maintainer review plus required OpenOnco clinical or language signoff. |
| Blocked | Requires banned source, restricted license, or patient-specific context. | Do not open as a TaskTorrent chunk. |

## Chunk Candidates

These are suitable first KB quality chunks:

| Chunk idea | Quality dimension | Output |
|---|---|---|
| Citation verification batch | Citation integrity | `citation-report.yaml` with supported / unsupported / ambiguous rows. |
| CIViC EID recheck | Citation integrity, drift | BMA sidecars or audit report tied to CIViC Evidence IDs. |
| Source recency refresh | Drift, source policy | Source stubs and stale-source report. |
| Duplicate BMA audit | Entity consistency | Duplicate report with canonical IDs and merge recommendations. |
| UA translation critical review | Localization quality | Translation review report and sidecar fixes where allowed. |
| Recommendation wording audit | Clinical reviewability | Report of overstrong or unsupported claims. |
| Coverage gap fill | Coverage | New sidecar drafts for missing entities, with strict manifest scope. |

## Acceptance Gates

A KB data-quality chunk should not be accepted unless:

- every touched entity is listed in `task_manifest.txt`
- output files stay inside `contributions/<chunk-id>/`
- every clinical claim references an allowed `SRC-*`
- every new source has a `source_stub` when required
- banned sources are absent
- schema validation passes after stripping `_contribution`
- reviewer can trace every recommendation to a source section, evidence ID, or
  explicit "unsupported / ambiguous" classification
- AI tool and model metadata are present
- high-risk content receives the consumer's required human signoff before hosted
  content is updated

## Metrics

Track these per release or audit wave:

- number of KB files scanned
- number of issues found by quality dimension
- number of issues converted into chunks
- number of chunks opened, merged, rejected, and deferred
- source-policy violations found
- duplicate entities found
- stale citations found
- unsupported claim rate
- human re-verification agreement rate
- average maintainer review time per chunk

## Operating Rules

- Reports can be merged as evidence of work without changing hosted content.
- Claim-bearing sidecars are drafts until maintainer upsert and signoff.
- Prefer smaller non-overlapping manifests over broad audit bundles.
- Do not use TaskTorrent for work a deterministic script can complete alone.
- Do not open more active chunks than maintainers can review within the SLA.
- Treat every rejection as a data point for improving the next chunk spec.

## Next Steps

1. Add a consumer-side quality dashboard or report script for OpenOnco.
2. Convert the highest-value findings into chunk specs under
   `chunks/openonco/`.
3. Open only the first one or two quality chunks while review throughput is
   measured.
4. Publish a short maintainer note explaining which issue classes are safe for
   external AI-assisted contributors.
5. Reuse the same quality dimensions when onboarding the next consumer project.
