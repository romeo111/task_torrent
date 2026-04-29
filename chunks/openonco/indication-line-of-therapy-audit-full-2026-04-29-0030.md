# Chunk: indication-line-of-therapy-audit-full-2026-04-29-0030

> Full audit of 302 indications: cited evidence vs claim line-of-therapy match.

## Status

`queued`

## Severity

`high`

## Min Contributor Tier

`trusted`

## Queue

`B`

## Topic Labels

`audit`, `indication`, `rct-fetch`

## Mission

B3 subset (PR #28) showed regex-only methodology insufficient — 29/30 ambiguous_source. This chunk runs the full audit on 302 IND with PubMed full-text fetch for cited Source.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > Indications with NCCN category` to verified-correct (current 100% nominal but unverified).

## Economic Profile

```yaml
compute_profile: mixed
verification_method: sample
break_even_test: PASS
output_type: report-only
verification_cost:
  maintainer_hours: 6
  expert_hours: 8
  expert_specialty: oncology
break_even_rationale: >
  302 INDs × ~12k tokens (fetch + parse + assess) = 3.6M tokens. Web fetch
  budget required (PubMed). Sample-verify 10% = 8h expert.
```

## Drop Estimate

~4 Drops (~400k tokens).

## Required Skill

`citation-verification`

## Allowed Sources

PubMed full-text + abstract, ClinicalTrials.gov, NCCN guidelines.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 302 INDs in `knowledge_base/hosted/content/indications/`. Manifest = full file list at activation.

## Output Format

- `contributions/indication-line-of-therapy-audit-full-2026-04-29-0030/audit-report.yaml`
- `contributions/indication-line-of-therapy-audit-full-2026-04-29-0030/task_manifest.txt`
- `contributions/indication-line-of-therapy-audit-full-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Per-IND row in audit-report.yaml with: claim line-of-therapy, cited source title/PMID, verdict (match / partial / mismatch / unfetchable).
- [ ] Severity classification per row.

## Rejection Criteria

- Verdict without fetched-source quote.
- Web fetch claims with no PMID.

## Verifier Threshold

>=85% claims pass Anthropic Citations API grounding (default).

## Claim Method

`trusted-agent-wip-branch-first`
