# Chunk: rec-wording-audit-claim-bearing

## Status

`queued`

## Topic Labels

`audit`, `semantic-NLU`, `report-only`

## Mission

Scan all claim-bearing free-text fields across BMA, Indication, Drug, RedFlag entities for forbidden recommendation wording (e.g. "best", "preferred", "first choice", "patients should", "we recommend"). Output: `audit-report.yaml` listing every offending field with the exact phrase, suggested neutral rewording, and severity.

OpenOnco's CHARTER §8.3 forbids LLM-as-clinical-decision-maker; the rule engine emits recommendations from declarative knowledge. Claim-bearing fields drift toward recommendation language under multi-agent drafting. This chunk is the systematic sweep.

## Drop Estimate

~10 Drops (~1.0M tokens). ~2000 entity files × ~500 tokens average per file scan + ~50 finding rows × ~2k tokens each for rewording suggestion.

## Required Skill

Audit-style semantic scanning (no formal skill spec yet — covered by output schema below).

## Allowed Sources

None. This chunk reads OpenOnco repo content only — no external sources cited or required.

## Manifest

All entities of type:

- `BiomarkerActionability` — fields `evidence_summary`, `evidence_summary_ua`, `notes`, `notes_patient` if present
- `Indication` — fields `rationale`, `notes`, `do_not_do`
- `Drug` — fields `mechanism`, `notes`, `notes_patient`
- `RedFlag` — fields `description`, `recommendation`, `notes`

Total scope: ~400 BMA + ~250 Indication + ~216 Drug + ~292 RedFlag = ~1158 entities × ~3 fields each ≈ 3400 fields scanned.

Maintainer commits the canonical `task_manifest.txt` listing entity stable IDs at chunk-issue open.

## Computation

For each entity in the manifest:

1. **Read** the entity YAML.
2. **For each scoped field**, scan for:
   - Direct recommendation verbs: "should", "must", "recommend", "advise", "prefer"
   - Superlative claims: "best", "first choice", "gold standard", "treatment of choice"
   - Patient-directed wording: "patients should", "the patient must", "you can"
   - Implied ranking: "first-line over X", "preferred to Y"
3. **Judgment per finding** — true positive vs false positive (e.g. "do not do" lists legitimately use "do not"). Token cost is in the judgment, not the regex — this is why it's an LLM task, not a grep.
4. **Rewording suggestion** — propose neutral phrasing: "evidence supports", "guidelines list", "source attests", "in cited trial".
5. **Severity tag**:
   - `critical` — direct treatment recommendation in claim-bearing field
   - `moderate` — superlative or implied ranking
   - `minor` — phrasing drift (e.g. "typically used" → "guideline-listed for")
6. **Append finding row** to `audit-report.yaml`.

## Where computation happens

Contributor's machine. Read-only access to `cancer-autoresearch` repo. No web access required.

## Re-verification

### Pre-acceptance gates (auto-reject)

- Schema validation on `audit-report.yaml`.
- Every `entity_id` and field path resolves to an entity in `task_manifest.txt`.
- `_contribution.ai_tool` and `_contribution.ai_model` present.

### Computational re-verify (cross-check with regex)

Maintainer runs a regex-based grep for the forbidden phrase patterns across the same manifest:

- If grep finds a phrase the contributor's report did NOT flag → **regression**: reject batch (contributor missed cases).
- If contributor flagged a phrase grep does NOT find → **valid catch**: contributor used semantic judgment beyond regex. No rejection (this is the LLM value-add).

The regex is a lower bound on what should be caught, not an upper bound.

### Sample human re-verify (5%)

Maintainer reads ~50 random findings:

- Confirm severity tag is appropriate.
- Confirm suggested rewording preserves clinical meaning.

### Trust threshold

- Regex-vs-report cross-check: 0 misses tolerated. Any grep hit not in report → reject batch.
- Sample severity tag agreement: ≥ 80%.
- Sample rewording quality: ≥ 80% maintainer-acceptable.

## Output Format

Single file: `contributions/rec-wording-audit-claim-bearing/audit-report.yaml`:

```yaml
_contribution:
  chunk_id: rec-wording-audit-claim-bearing
  contributor: github-username
  ai_tool: <tool>
  ai_model: <model>
  ai_model_version: ""
  ai_session_notes: ""
  notes_for_reviewer: ""

findings:
  - finding_id: f-001
    entity_id: IND-NSCLC-1L-EGFR-OSIMERTINIB
    field_path: "rationale"
    excerpt: "Osimertinib is the best 1L choice for EGFR-mutant NSCLC."
    matched_pattern: "best 1L choice"
    severity: critical
    suggested_rewording: "Guidelines list osimertinib as a 1L option for EGFR-mutant NSCLC (NCCN Cat 1, ESMO MCBS A)."
    notes: "Recommendation phrasing 'best choice' violates CHARTER §8.3 LLM-as-decider boundary."
```

## Acceptance Criteria

- Gates pass.
- Regex cross-check: 0 misses.
- Sample re-verify ≥ 80% on both severity and rewording quality.

## Rejection Criteria

- Regex cross-check finds patterns not in report.
- Severity tags inconsistent (e.g. "patients should switch to X" tagged `minor`).
- Rewording suggestions invent clinical claims not present in original.

## Claim Method

`trusted-agent-wip-branch-first` — see `docs/chunk-system.md` §"Claim Method".

## Reviewer

- Maintainer: 1.
- Clinical Co-Lead signoff: not required for the report. Subsequent maintainer rewording edits in hosted content follow CHARTER §6.1.
