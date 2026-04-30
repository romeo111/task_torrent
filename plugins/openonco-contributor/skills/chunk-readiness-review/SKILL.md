---
name: chunk-readiness-review
description: Review a TaskTorrent v0.4 chunk spec (typically an OpenOnco chunk under `chunks/openonco/<id>.md`) before a contributor claims it or before a maintainer opens the issue. Reports blocking issues, warnings, source-policy notes, and manifest-concreteness checks. Does not modify chunk specs and does not open issues.
---

# Skill: Chunk Readiness Review

## Purpose

Help maintainers and contributors decide whether a chunk is ready to open or claim by comparing it to TaskTorrent v0.4 protocol requirements. This skill produces a review checklist; it does not edit chunk specs and does not open GitHub issues.

## Source of Truth — RUN THE LINTER, DO NOT PARAPHRASE IT

The required chunk shape is enforced by the linter at `tasktorrent/lint_chunk_spec.py`. **Always run the linter before reporting blocking issues** — do not infer what the linter would say from memory or from reading the source. The model's read of "required sections" or "valid tokens" is unreliable; the linter's exit code and output are authoritative.

Before producing your report:

1. Run the linter on the target chunk via the Bash tool:
   ```bash
   python -m tasktorrent.lint_chunk_spec <path-to-chunk.md>
   ```
2. Capture the exit code and output. Treat any `FAIL` line as a blocking issue and quote it verbatim. Treat `WARNING` lines as warnings.
3. Only after the linter has run should you add review-quality observations the linter does not check (manifest concreteness, scope alignment, source-policy semantics, safety-boundary language).

If the Bash tool is not available in the current session, say so explicitly in your report and mark all linter-derived checks as "deferred — run `python -m tasktorrent.lint_chunk_spec <path>` manually." Do not invent linter findings.

Read the linter's authoritative lists from the file (via the Read tool) when you need to cite valid tokens. Do not paraphrase from memory. Lists you'll likely consult:

- `REQUIRED_SECTIONS` — sections every chunk must have
- `SOFT_REQUIRED_SECTIONS_V0_5` — sections that emit warnings under v0.4 and become required under v0.5
- `VALID_STATUS`, `VALID_CLAIM_METHODS`, `VALID_BREAK_EVEN_TESTS`, `VALID_COMPUTE_PROFILES`, `VALID_VERIFICATION_METHODS`, `VALID_SEVERITY`, `VALID_MIN_TIER`, `VALID_QUEUE`
- `CITATION_TOPIC_LABELS` — chunks tagged with these must declare a Verifier Threshold

A chunk that the linter passes (`PASS chunks/openonco/<id>.md`) cannot have linter-derived blocking issues. If your report claims one, the linter wins — fix your report.

## When To Use

Use this skill when:

- a maintainer asks "is this chunk ready to open?"
- a contributor asks "is this chunk safe to claim?"
- a reviewer is doing a pre-issue lint pass on a draft chunk

Do not use this skill to:

- modify chunk specs (the user must apply fixes themselves)
- open or claim issues automatically

## Review Checklist

Run through these in order. Separate **blocking** issues from **warnings** in the output.

### 1. Required sections present (BLOCKING)

Every section in `REQUIRED_SECTIONS` must exist with non-empty content. Missing or stub sections are blocking.

### 2. Status / claim method tokens valid (BLOCKING)

- `Status` must be one of `VALID_STATUS`.
- `Claim Method` must be one of `VALID_CLAIM_METHODS`.

### 3. Economic Profile YAML valid (BLOCKING)

The Economic Profile section must contain a YAML block declaring:

- `break_even_test` ∈ `VALID_BREAK_EVEN_TESTS`
- `compute_profile` ∈ `VALID_COMPUTE_PROFILES`
- `verification_method` ∈ `VALID_VERIFICATION_METHODS`

`MARGINAL` chunks must additionally declare `expected_violations` (Proposal #20). Volume-mutating chunks must declare `volume_impact` (Proposal #18).

### 4. Manifest concreteness (BLOCKING)

The Manifest section must list concrete entity IDs or filename ranges, not placeholders. Reject:

- `entity_ids: TBD`
- `manifest: <to be filled>`
- empty bullet lists

### 5. Allowed Sources / source policy (BLOCKING)

For OpenOnco chunks specifically:

- The Allowed Sources list must be a subset of the OpenOnco source allowlist in `docs/openonco-pilot-workflow.md`.
- The chunk must not list banned sources (OncoKB, SNOMED CT, MedDRA) as allowed.
- If the chunk involves citation work, it should reference the verifier and source-policy expectations.

### 6. Output Format / sidecar path (BLOCKING)

Output Format must specify:

- The exact `contributions/<chunk-id>/...` path or path pattern
- Filename convention (one entity per file when applicable)
- Wrapper / `_contribution` block requirement when sidecars apply

### 7. Drop Estimate (BLOCKING)

Must be a non-empty estimate. A bare "TBD" is blocking. A range like "8–12 Drops" is acceptable; specify how the estimate was derived if unusual.

### 8. Acceptance / Rejection criteria (BLOCKING)

Both must be specific and machine-checkable where possible. Vague criteria (e.g. "high quality") are blocking.

### 9. Soft-required v0.5 sections (WARNING under v0.4)

Sections in `SOFT_REQUIRED_SECTIONS_V0_5` (`Severity`, `Min Contributor Tier`, `Queue`) emit warnings under v0.4 and will be blocking in v0.5. Recommend backfilling now.

### 10. Verifier Threshold for citation chunks (WARNING)

If any topic label in `CITATION_TOPIC_LABELS` is set, the chunk should declare a Verifier Threshold (Proposal #23). Missing threshold → warning.

### 11. Safety boundary language (WARNING)

For OpenOnco chunks, look for explicit language stating:

- contributors do not edit `knowledge_base/hosted/content/`
- no treatment advice, no patient-specific output
- one chunk = one PR

If absent, recommend adding to the Rules section.

## Output Format

Produce a markdown report:

```markdown
## Chunk Readiness Review — <chunk-id>

Source: chunks/openonco/<chunk-id>.md
Reviewer: claude (chunk-readiness-review skill)
Date: <YYYY-MM-DD>

### Blocking issues
- ...

### Warnings
- ...

### Source policy notes
- ...

### Manifest notes
- ...

### Validation plan
- `python -m tasktorrent.lint_chunk_spec chunks/openonco/<chunk-id>.md`
- `python -m pytest tests/test_lint_chunk_spec.py -q`
```

If there are no blocking issues, say so explicitly. Do not promise the chunk is "ready" without running the linter — defer to it.

## Rules

- **Run the linter, do not paraphrase it.** Every blocking issue derived from required-section / valid-token rules must be backed by an actual linter `FAIL` line you observed. If you did not run the linter, mark those checks as deferred and say so.
- Do not edit the chunk spec. The reviewer or contributor applies fixes.
- Do not open issues automatically. If the user explicitly asks, surface the chunk URL and stop.
- Distinguish blocking from warning. Mixing them up wastes maintainer time.
- Quote the exact section / line you are flagging. "Manifest is vague" is not actionable; "`Manifest:` line 14 says `TBD`" is.
- Defer to `tasktorrent/lint_chunk_spec.py` when the linter and your read disagree. The linter is the canonical decision; your job is to add the review-quality observations the linter does not check.

## Good Output

- A short report with concrete file:line references and a clear blocking/warning split.
- A validation command the user can run themselves.
- A "no blocking issues, ready to lint" verdict only when every required section passes.

## Bad Output

- "Looks fine" with no concrete checks.
- Marking warnings as blocking (or vice versa) without justification.
- Editing the chunk spec to "fix" issues.
- Re-implementing the linter inline instead of pointing at it.
