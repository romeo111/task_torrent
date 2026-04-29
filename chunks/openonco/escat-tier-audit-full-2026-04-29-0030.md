# Chunk: escat-tier-audit-full-2026-04-29-0030

> Full ESCAT audit of all 399 BMAs (B2 subset projected ~76% mismatch on 50 sample).

## Status

`queued`

## Severity

`high`

## Min Contributor Tier

`trusted`

## Queue

`B`

## Topic Labels

`audit`, `civic-evidence`, `claim-bearing`

## Mission

B2 subset audit (PR #28) showed 38/50 BMAs with ESCAT mismatch (16 overclaim + 22 underclaim). This chunk audits ALL 399 BMAs against ESCAT v1 (Mateo et al. 2018). Output: per-BMA proposed tier correction with rationale.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > BMA with ESCAT tier` from nominal 100% to verified-correct ~70%, exposing the actual ground-truth tier accuracy.

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: sample
break_even_test: PASS
output_type: report-only
verification_cost:
  maintainer_hours: 8
  expert_hours: 16
  expert_specialty: molecular-oncology
break_even_rationale: >
  B2 projected ~140 overclaim + 175 underclaim across 399. Manual full
  audit = 100h. Contributor ~830k tokens. Expert sample-verify 10% (40
  BMAs) = 16h.
```

## Drop Estimate

~8 Drops (~800k tokens).

## Required Skill

`biomarker-extraction`

## Allowed Sources

ESMO ESCAT v1 (Mateo 2018), CIViC, NCCN/ESMO disease-specific.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 399 BMAs in `knowledge_base/hosted/content/biomarker_actionability/`. Manifest is the full file list (run `ls` against that dir at activation time).

## Output Format

- `contributions/escat-tier-audit-full-2026-04-29-0030/audit-report.yaml` — single report
- `contributions/escat-tier-audit-full-2026-04-29-0030/task_manifest.txt`
- `contributions/escat-tier-audit-full-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] audit-report.yaml lists every BMA-* with current_tier, proposed_tier, rationale.
- [ ] Per-BMA rationale cites the ESCAT criterion that drives the verdict.
- [ ] Severity classification (critical / moderate / minor) on every row.

## Rejection Criteria

- Tier change without rationale.
- Generic 'should be IIA' without ESCAT criterion.

## Claim Method

`trusted-agent-wip-branch-first`
