# Chunk: trial-source-ambiguous-resolution-2026-04-29-0030

> Resolve 22 ambiguous trial names from B1 false-positive filter (deferred by Codex in PR #29).

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`B`

## Topic Labels

`source-ingest`, `metadata-classification`, `audit`

## Mission

PR #29 ingested 25 confirmed-real trials and skipped 22 ambiguous ones (CROSS, PARADIGM, RUBY, CODEBREAK, AIDA, PROPEL, MAGNITUDE, THOR, etc.) for maintainer review. This chunk resolves each: real RCT (ingest as SRC stub) vs false-positive (mark in extracted-trials list).

**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > Sources` — completes the trial-source-ingest workstream.

## Economic Profile

```yaml
compute_profile: mixed
verification_method: sample
break_even_test: PASS
output_type: mixed
verification_cost:
  maintainer_hours: 1
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  22 trials × ~7k tokens (PubMed + license read) = ~150k. Sample-verify
  30%.
```

## Drop Estimate

~1 Drops (~100k tokens).

## Required Skill

`citation-verification`

## Allowed Sources

PubMed E-utilities, ClinicalTrials.gov, journal landing pages.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

22 trial-name candidates from PR #29's `Deferred / not stubbed in this slice`:

`CROSS, PARADIGM, RUBY, CODEBREAK, AIDA, PROPEL, MAGNITUDE, THOR, ARASENS, PRODIGE, BFORE, FIRE-3, ICON7, STARTRK, STUPP, AGILE, STIL, CRYSTAL, MONUMENTAL-1, BRIGHT, IMPOWER150, SHINE`.

## Output Format

- `contributions/trial-source-ambiguous-resolution-2026-04-29-0030/source_stub_*.yaml` — for confirmed real
- `contributions/trial-source-ambiguous-resolution-2026-04-29-0030/false_positive_resolution_report.yaml` — for confirmed-false
- `contributions/trial-source-ambiguous-resolution-2026-04-29-0030/task_manifest.txt`
- `contributions/trial-source-ambiguous-resolution-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Each of the 22 trial names is resolved: stub OR false-positive entry.
- [ ] Stubs follow PR #29 schema (license + 4 permission booleans + hosting_mode: referenced).
- [ ] L-13 title-substring check passes for stubs.

## Rejection Criteria

- L-13 title-substring fail.
- Trial unresolved (no verdict).

## Verifier Threshold

>=85% claims pass Anthropic Citations API grounding (default).

## Claim Method

`formal-issue`
