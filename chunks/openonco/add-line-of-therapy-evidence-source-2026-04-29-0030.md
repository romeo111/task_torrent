# Chunk: add-line-of-therapy-evidence-source-2026-04-29-0030

> Add `line_of_therapy_evidence_source` field to all 302 IND, citing the specific RCT that established the line.

## Status

`queued`

## Severity

`medium`

## Min Contributor Tier

`trusted`

## Queue

`C`

## Topic Labels

`schema-evolution`, `indication`, `rct-fetch`

## Mission

Indications currently set `evidence_level: high|moderate|low` and `nccn_category: '2A'` but don't tie the line-of-therapy to a specific RCT. Add `line_of_therapy_evidence_source: SRC-*` per IND.

**KB coverage:** Advances `kb-coverage-matrix.md > Quality scores > Indications with NCCN category` quality dimension (citation-traceable LoT).

## Economic Profile

```yaml
compute_profile: mixed
verification_method: full-expert
break_even_test: PASS
output_type: entity-sidecar
verification_cost:
  maintainer_hours: 6
  expert_hours: 12
  expert_specialty: oncology
break_even_rationale: >
  302 INDs × ~10k tokens = 3M. Schema upsert is mechanical; selecting the
  right RCT per LoT requires clinical judgment + sometimes new SRC stubs.
```

## Drop Estimate

~3 Drops (~300k tokens).

## Required Skill

`drug-evidence-mapping`

## Allowed Sources

PubMed pivotal trial readouts, NCCN guidelines, existing SRC-* registry.

## Disallowed Sources

`SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`.

## Manifest

All 302 INDs. Pre-activation `ls knowledge_base/hosted/content/indications/`. Final manifest = 302 IND-* IDs in `task_manifest.txt`.

## Output Format

- `contributions/add-line-of-therapy-evidence-source-2026-04-29-0030/ind_<id>.yaml` — upsert each
- `contributions/add-line-of-therapy-evidence-source-2026-04-29-0030/source_stub_*.yaml` — new SRC stubs as needed
- `contributions/add-line-of-therapy-evidence-source-2026-04-29-0030/task_manifest.txt`
- `contributions/add-line-of-therapy-evidence-source-2026-04-29-0030/_contribution_meta.yaml`

## Acceptance Criteria

- [ ] ai_tool + ai_model.
- [ ] Every IND has `line_of_therapy_evidence_source` pointing at SRC-* (existing or new stub).
- [ ] L-13 title-substring check passes for any new SRC stubs.
- [ ] Per-IND `notes_for_reviewer` cites specific trial section.

## Rejection Criteria

- Generic guideline citation when a specific RCT is the actual source.
- L-13 fail.

## Verifier Threshold

>=85% claims pass Anthropic Citations API grounding (default).

## Claim Method

`trusted-agent-wip-branch-first`
