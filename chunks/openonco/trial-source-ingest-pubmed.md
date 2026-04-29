# Chunk: trial-source-ingest-pubmed

## Status

`queued`

## Verifier Threshold

>=85% claims pass Anthropic Citations API grounding (default).

## Queue

`A`

## Min Contributor Tier

`established`

## Severity

`medium`

## Topic Labels

`source-ingest`, `metadata-classification`, `pubmed-fetch`

## Mission

Ingest pivotal-trial Source entities for the unique RCTs identified by `citation-semantic-verify-v2`'s `source_stub_needed` rows. Output: per-trial `source_stub_<id>.yaml` for new SRC-* entries, with PubMed-confirmed citation + license classification + attribution. Feeds maintainer-led source promotion via `specs/SOURCE_INGESTION_SPEC.md` §8.

The trial-extraction list (`cancer-autoresearch/contributions/citation-semantic-verify-v2/trials-needing-source-ingest.md`) names 47 unique trial-name candidates. **At least some are false positives** (Codex labeled generic words like "CROSS"/"PARADIGM" as trial names where v1 audit had no clear trial). This chunk's first sub-task is filtering real trials from false positives BEFORE PubMed lookup.



**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > Sources` — ingests pivotal-trial Source entities for un-stubbed RCT references.
## Economic Profile

```yaml
compute_profile: mixed
llm_essential_pct: 50
script_alternative:
  exists: partial
  path: null
  rationale: >
    PubMed search via NCBI E-utilities is scriptable. Title parsing + DOI
    extraction also scriptable. The LLM-essential parts are: (1) judging
    whether a "trial name" candidate is a real RCT or a false positive,
    (2) license classification (reading publisher terms-of-use pages and
    mapping to SPDX/CC0/restricted), (3) deciding stable ID + attribution.
    Could be hybrid (Python script does PubMed fetch; LLM step does
    classification per result). Current chunk does both via LLM for
    simplicity.

verification_method: sample
verification_cost:
  maintainer_hours: 2   # 20% sample on license-accuracy (5-10 stubs)
  expert_hours: 0       # source stubs not claim-bearing
  expert_specialty: ""

break_even_test: PASS
break_even_rationale: >
  ~47 candidate trials × manual PubMed-lookup-and-stub-authoring would
  take maintainer ~10 hours. LLM contributor at ~5k tokens/trial =
  ~250k tokens. Sample-verify 20% (10 stubs) = 2 maintainer-hours. Net
  win: ~8 maintainer-hours saved. License-classification mistakes are
  high-stakes (can violate publisher ToS), so the 20% sample-verify is
  important + non-negotiable.

compute_classification: mixed
output_type: entity-sidecar
```

## Drop Estimate

~3 Drops (~300k tokens). 47 candidate trials × ~6k tokens (false-positive filter + PubMed search + parse + license read + stub author).

## Required Skill

`citation-verification` (license classification + metadata extraction).

## Allowed Sources

PubMed E-utilities, journal landing pages (for license terms), CIViC (where trials have CIViC EIDs). For NCCN/ESMO/ASCO, cite by reference only — do not stub a guideline as a trial.

## Manifest

`cancer-autoresearch/contributions/citation-semantic-verify-v2/trials-needing-source-ingest.md` — 47 candidate trial names + per-trial finding_id list. Maintainer commits canonical `task_manifest.txt` listing the 47 trial names + which `source_stub_needed` finding_ids they cover.

Contributor's first task: pre-filter the 47 candidates into:
- **Likely real RCT** (most-cited and recognizable: PARADIGM, CROSS in real domain, KEYNOTE-* if present, etc.) → proceed to PubMed lookup
- **Likely false positive** (single-citation, generic word, no trial signature) → produce a `false_positive_report.yaml` row, no stub
- **Ambiguous** → mark `maintainer_review_needed`, no stub

The pre-filter is itself an audit. ~50% of the 47 may be false positives — that's expected.

## Computation

For each candidate trial in the manifest:

1. **False-positive filter:** does the trial name look like a real RCT acronym? Check:
   - Is it a known multi-character acronym (KEYNOTE-XXX, CHECKMATE-XXX, IMpower-XXX, MAGNITUDE, etc.)?
   - Is it cited across multiple unrelated disease domains? (Single-domain → likely real; many-domain → likely generic word.)
   - Is it a generic English word that could be misread as a trial name (CROSS, PARADIGM, THOR — these CAN be real trials but require domain check)?
2. **For pre-filtered real candidates: PubMed search.**
   - Query: `<trial name>[All Fields] AND clinicaltrial[Filter]` or domain-specific.
   - Pick pivotal publication (highest-impact journal, lead author named, RCT design).
3. **Extract metadata:** title, authors (first 3 + et al.), journal, year, volume, pages, DOI, PMID.
4. **License classification:** open the journal's permissions page. Map to SPDX where possible. Set `commercial_use_allowed`, `redistribution_allowed`, `modifications_allowed`, `sharealike_required` booleans honestly.
5. **Build attribution.text:** verbatim citation per journal's attribution requirement.
6. **Decide stable ID:** `SRC-<TRIAL>-<LEAD-AUTHOR>-<YEAR>` per OpenOnco convention.
7. **Write sidecar** at `contributions/trial-source-ingest-pubmed/source_stub_src_<trial>_<author>_<year>.yaml` with `_contribution.target_action: new`.

## Where computation happens

Contributor's machine. Required:
- Web access (PubMed, journal landing pages).
- Read access to cancer-autoresearch (existing `SRC-*` registry to avoid duplicates).

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on every stub.
- Every stub's `id` is genuinely new (no collision).
- `license` block is non-empty.
- All 4 license-permission booleans explicitly set.
- `hosting_mode: referenced`.
- For each stub: `pmid` resolves via PubMed (HTTP HEAD on `https://pubmed.ncbi.nlm.nih.gov/<pmid>/`).
- For each stub: trial name (extracted from title) matches the candidate name.

### Computational re-verify

Maintainer runs `reverify_citation_replace_source.py` (already in repo) — title-substring check from claim → target SRC-*. Plus URL HEAD on `Source.url`.

### Sample human re-verify (20%)

Maintainer reads ~10 random stubs, confirms:
- License classification matches the source's stated license.
- `precedence_policy` is appropriate (most pivotal trials = `secondary_evidence_base` or `confirmatory`; not `leading`).
- Attribution string is verbatim.
- No false-positive trials slipped through (e.g., CROSS being stubbed as a colorectal trial when entity context is FLT3 AML).

### Trust threshold

- Gates: 100%.
- License accuracy on sample: 100% (license errors are blocking; wrong classification could violate publisher terms).
- False-positive filter accuracy: ≥ 90% (i.e., maintainer agrees with at least 90% of the "real RCT" pre-filter calls).

## Output Format

- `contributions/trial-source-ingest-pubmed/source_stub_src_<trial>_<author>_<year>.yaml` — one per real trial
- `contributions/trial-source-ingest-pubmed/false_positive_report.yaml` — list of pre-filtered false positives with rationale
- `contributions/trial-source-ingest-pubmed/task_manifest.txt`
- `contributions/trial-source-ingest-pubmed/_contribution_meta.yaml`

## Acceptance Criteria

- All gates pass.
- Sample license accuracy 100%.
- False-positive filter ≥ 90% maintainer agreement.

## Rejection Criteria

- License errors (wrong classification of restricted source as open).
- Stubbing a guideline as a trial.
- Stubbing for a false positive (e.g., a `SRC-CROSS-FLT3-AML` stub that doesn't correspond to a real RCT).
- Hosting mode proposed by contributor.

## Claim Method

`formal-issue` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1 (sample-verify license + filter accuracy).
- No Clinical Co-Lead signoff for stubs themselves; full Source promotion via `specs/SOURCE_INGESTION_SPEC.md` §8 separately.
