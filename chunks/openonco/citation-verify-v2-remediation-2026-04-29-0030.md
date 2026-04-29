# Chunk: citation-verify-v2-remediation-2026-04-29-0030

> Apply citation-verify-v2's 793 actionable findings: replace_source / new-source / source-stub.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`established`

## Queue

`B`

## Topic Labels

`citation-verify`, `remediation`

## Mission

citation-verify-v2 (PR #23) produced 793 actionable rows. Apply each: for `replace_source` rows, swap the cited SRC-* (verifier title-substring check from L-13 must pass); for `source_stub_needed`, file a SRC-* stub; for ambiguous, mark `maintainer_review_needed`.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > Sources current_as_of <365d` indirectly (newly stubbed sources have fresh metadata).

## Economic Profile

```yaml
compute_profile: llm-essential
verification_method: computational
break_even_test: PASS
output_type: mixed
verification_cost:
  maintainer_hours: 4
  expert_hours: 0
  expert_specialty: 
break_even_rationale: >
  793 rows × ~5k tokens = 4M tokens. But L-13 title-verify is automated
  (computational re-verify is the gate, not human review). Maintainer 4h
  to run reverify_citation_replace_source + spot-check.
```

## Drop Estimate

~4 Drops (~400k tokens).

## Required Skill

`citation-verification`

## Allowed Sources

PubMed, journal landing pages, existing SRC-* registry.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

793 rows from `cancer-autoresearch/contributions/citation-semantic-verify-v2/citation-semantic-verify-report.yaml` (status: actionable). Final manifest = 793 row IDs as `task_manifest.txt`.

## Output Format

- `contributions/citation-verify-v2-remediation-2026-04-29-0030/<entity-id>.yaml` — entity upserts
- `contributions/citation-verify-v2-remediation-2026-04-29-0030/source_stub_*.yaml` — new SRC stubs
- `contributions/citation-verify-v2-remediation-2026-04-29-0030/task_manifest.txt`
- `contributions/citation-verify-v2-remediation-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Every replace_source row passes `reverify_citation_replace_source.py` title-substring check.
- [ ] Every new SRC stub has full license block + 4 permission booleans.
- [ ] Hosting mode `referenced` for all stubs.
- [ ] No `SRC-CROSS-FLT3-AML`-style false-positive stubs.

## Rejection Criteria

- L-13 title-substring fail (any row).
- Banned source stubbed.

## Verifier Threshold

>=95% replace_source rows pass title-substring check (stricter than default 85% because lexical-match risk per L-13).

## Claim Method

`trusted-agent-wip-branch-first`
