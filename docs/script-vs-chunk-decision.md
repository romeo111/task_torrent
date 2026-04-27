# Script vs Chunk Decision Tree

Before opening a chunk-task issue, walk this tree. If you land on **WRITE A SCRIPT**, do not open a chunk.

## Tree

```
START
  │
  ├── Q1: Could a Python script with access to {repo + standard libs + project APIs}
  │       produce equivalent output?
  │
  ├── YES, fully equivalent ────────────────────────────► WRITE A SCRIPT.
  │     (script_alternative: yes)                          The "free contributor tokens"
  │                                                        argument doesn't apply because
  │                                                        verification cost dominates.
  │
  ├── YES, with manual touch-up at the end (e.g. notes ──► WRITE A SCRIPT + 1 LLM step.
  │     for reviewer, edge-case handling)                  Don't ship the whole task as
  │     (script_alternative: partial, llm_essential       a chunk just to capture the 5%
  │      < 30%)                                            judgment.
  │
  ├── PARTIALLY (regex-floor + semantic catch, ──────────► CHUNK if llm_essential ≥ 50%
  │     bilingual review, fuzzy synthesis)                  AND verification is cheap
  │     (script_alternative: partial, llm_essential       (sample-check, automated
  │      30–70%)                                           cross-check). Else SCRIPT.
  │
  └── NO, the work is genuinely LLM-only ───────────────► CHUNK if break-even test passes.
        (script_alternative: no, llm_essential 70+%)       See Q2 below.

Q2: If chunking, does verification cost stay below contributor value?
  │
  ├── verification = automated + sample (≤10%) ──────────► PASS. Open chunk.
  │
  ├── verification = sample + UA-clinician / Co-Lead ────► PASS only if work scale
  │     for partial review                                 justifies (e.g. 1000+
  │                                                        rows where bilingual
  │                                                        clinician reads 15%).
  │
  ├── verification = full-expert-review (100%) ─────────► MARGINAL. Open only if
  │                                                        the draft itself saves
  │                                                        substantial expert time
  │                                                        (Co-Lead reviews-and-edits
  │                                                        faster than drafting
  │                                                        from scratch).
  │
  └── verification = full-expert-review at high stakes ──► FAIL. The expert may as
        (every row / claim must be re-derived from        well do the work directly
        scratch by Co-Lead)                               — no Cohen-Bender saving.
```

## Concrete examples (from OpenOnco pilot)

| Chunk | Script alternative? | Verification | Break-even | Verdict |
|---|---|---|---|---|
| `civic-bma-reconstruct-all` | Yes (`reconstruct_bma_evidence_via_civic.py`) | 100% Co-Lead | FAIL | Should have been a script. We learned this AFTER spending ~1M tokens. |
| `citation-verify-914-audit` | No (semantic NLU) | 10% sample | PASS | Clear win. |
| `rec-wording-audit-claim-bearing` | Partial (regex floor) | Regex cross-check + 5% sample | PASS | Hybrid script + LLM works; chunk does both in one pass. |
| `ua-translation-review-batch` | No (bilingual) | Untranslated-fragment auto-detect + 15% UA-clinician | PASS | Clear win — but expensive to verify (Ukrainian clinician needed). |
| `bma-drafting-gap-diseases` | No (synthesis) | 100% Co-Lead | MARGINAL | Drafts save time only if Co-Lead accepts ≥ 70% with minor edits. |
| `redflag-indication-coverage-fill` | No (clinical judgment) | 100% Co-Lead, 2-of-3 | MARGINAL | Same as above; higher stakes (claim-bearing). |
| `source-stub-ingest-batch` | Partial (license parse) | 20% sample | PASS | License classification is the hard part; LLM scales it. |

## Anti-patterns to avoid

1. **Chunk-as-script-substitute.** Chunk exists because writing a script feels harder than writing a chunk spec. Wrong: write the script, not the chunk spec.
2. **Chunk-as-batch-processor.** "I have 500 mechanical things to do; let's chunk it." If each thing is mechanical, multiplication doesn't help — it's still scripted work.
3. **Chunk-with-100%-expert-review and no contributor-side judgment value.** The expert is just re-doing the work; LLM adds no leverage.
4. **Chunk-without-break-even-calc.** Verification cost is hand-waved; "we'll figure it out post-merge." That's how pilot's first chunk burned tokens for net-negative outcome.

## When to revisit a FAIL chunk

- Script-alternative cost dropped (someone wrote the script).
- Verification cost dropped (automated re-verify became feasible).
- Work scope changed (the un-scriptable part became dominant).

If revisiting a FAIL chunk, keep the original FAIL marker as institutional memory; add a "revisited because X" note when re-classifying.
