# Safety Rules

## No Medical Advice

TaskTorrent contributors must not provide medical advice. Outputs should be structured drafts for maintainer review, not guidance for patients or clinicians.

## No Treatment Recommendations

OpenOnco and similar health-related chunks must not ask contributors to decide the best treatment, rank treatments, or write recommendation wording.

Allowed work includes evidence mapping, citation verification, data normalization, and clearly sourced summaries for review.

## No Patient-Specific Outputs

Contributors must not generate patient-specific interpretations, diagnoses, treatment options, or risk assessments.

## Source Links Required

Every clinical claim must include source links. Claims without sources should be marked as unsupported or unclear, not rewritten as fact.

## No Fake Citations

Contributors must not invent sources, infer source support without checking, or use placeholder citations as if they are real.

## Source Allowlist (OpenOnco pilot)

For OpenOnco chunks, only these source types are allowed:

- **CIViC** (CC0) — primary actionability source.
- **ClinicalTrials.gov** (public domain) — trial protocols and outcomes.
- **PubMed abstracts and PMC Open Access full-text** — confirm OA license per article.
- **DailyMed and openFDA** (public domain) — FDA-curated drug labels and AE data.
- **ESMO / ASCO open guidelines** — cite section + version.
- **NCCN guidelines** — cite by reference only (no guideline text in the repo).
- **WHO Classification of Tumours** — cite by reference only.
- **МОЗ України** orders — Ukrainian Ministry of Health protocols.

Banned for the pilot:

- **OncoKB** — ToS conflicts with OpenOnco's free public / non-commercial CHARTER §2.
- **SNOMED CT** and **MedDRA** — license-gated.

Paywalled full-text journal articles: abstract-only support is acceptable when the chunk explicitly authorizes it; mark `support_status: unclear` if abstract is insufficient. See `docs/openonco-pilot-workflow.md` §"Source allowlist" for the maintained version of this table.

## Maintainer Review Required

All AI-generated outputs require maintainer review before publication or merge. A pull request, file, or report is a draft until maintainers approve it.

## Citation Grounding Verification

For consumer repos that ship clinical content, every contributor PR that touches
sidecars MUST pass an automated citation-grounding verifier before maintainer
review. Reference implementation:
[`cancer-autoresearch/scripts/tasktorrent/verify_citations.py`](https://github.com/romeo111/OpenOnco/blob/master/scripts/tasktorrent/verify_citations.py)
+ [`citation-verify` workflow](https://github.com/romeo111/OpenOnco/blob/master/.github/workflows/citation-verify.yml).

The verifier is **obligatory pre-merge gate** for OpenOnco-style consumers. It runs
three layers:

1. **Structural** (always blocking): every cited `SRC-*` exists on master OR is
   stubbed in the chunk dir; every CIViC EID matches the snapshot.
2. **Title-substring** (always blocking): when a claim mentions `trial XYZ` /
   `study XYZ`, the trial name must appear in at least one cited source's
   title or notes. Lexical-matching against arbitrary `SRC-*` IDs without
   title verification has produced false positives in production
   (see `docs/tasktorrent-improvement-plan.md` L-13).
3. **Semantic** (opt-in): Claude API scores grounding 0-1; fails only on
   `grounded=false AND confidence ≥ 0.7`. Requires `ANTHROPIC_API_KEY`
   secret. Forks without the key skip this layer gracefully — never
   block on missing secrets.

The semantic check is the canonical adjudicator for ambiguous cases.
Two-agent disagreement on a claim → flag for maintainer review, never
auto-merge.

Skill spec: [`skills/citation-verification.md`](../skills/citation-verification.md).

## Rejection Rules

Maintainers should reject or request changes when an output:

- Gives medical advice
- Uses treatment recommendation wording
- Contains patient-specific guidance
- Makes clinical claims without source links
- Includes fake or unverifiable citations
- Fails the citation grounding verifier (any layer)
- Exceeds the assigned chunk scope
- Rewrites unrelated content
