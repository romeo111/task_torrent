# Chunk: regimen-outcome-fill-2026-04-29-0030

> Backfill `expected_outcomes` (median OS, ORR, CR rate) for 50 regimens currently lacking.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`A`

## Topic Labels

`regimen-data`, `outcomes`, `rct-fetch`

## Mission

Of 244 regimens in the KB, an unknown number lack structured `expected_outcomes` blocks (median OS, ORR, CR, PFS). This chunk samples 50 high-traffic regimens and backfills outcomes data from their pivotal trial citations.

**KB coverage:** Advances `kb-coverage-matrix.md > Top-level KPIs > Regimens` quality dimension (regimens with outcomes data — currently unmeasured; this chunk + audit chunk #15 establish the baseline).

## Economic Profile

```yaml
compute_profile: mixed
verification_method: sample
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 4
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  Manual outcomes extraction = ~10 min/regimen × 50 = 8.3h. Contributor at
  ~10k tokens/regimen = 500k tokens. Sample-verify 20% = 4h.
```

## Drop Estimate

~2 Drops (~200k tokens).

## Required Skill

`drug-evidence-mapping`

## Allowed Sources

PubMed (pivotal trial readouts), ClinicalTrials.gov, FDA labels.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

50 regimen IDs to be selected by maintainer prior to chunk activation, weighted toward:

- High-traffic regimens (BMA / IND back-references)
- Regimens currently lacking `expected_outcomes`
- Regimens with single pivotal RCT (clearer extraction)

Final manifest committed as `task_manifest.txt` listing 50 stable REG-* IDs.

## Output Format

- `contributions/regimen-outcome-fill-2026-04-29-0030/reg_<id>.yaml` — one per regimen (upsert)
- `contributions/regimen-outcome-fill-2026-04-29-0030/task_manifest.txt`
- `contributions/regimen-outcome-fill-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Each upsert preserves existing fields, adds `expected_outcomes` block.
- [ ] `expected_outcomes` cites a specific pivotal trial in `notes_for_reviewer`.
- [ ] OS/PFS values match cited source's reported numbers.

## Rejection Criteria

- Made-up OS values without citation.
- Cross-trial number mixing.

## Claim Method

`formal-issue`
