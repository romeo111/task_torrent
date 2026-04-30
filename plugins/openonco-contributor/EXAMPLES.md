# EXAMPLES

Six examples of how to use the OpenOnco TaskTorrent contributor
plugin: three safe paths, two unsafe-request refusals, and one
"between-wave / no claimable chunk" path.

All examples assume the plugin is installed (see [SETUP.md](./SETUP.md))
and the user has a local checkout of `romeo111/task_torrent` and
`romeo111/OpenOnco`.

---

## Example 1 — Safe citation verification

**User prompt:**

```text
/openonco-contribute

I want to take a citation-verification chunk if one is open. I have
romeo111/task_torrent and romeo111/OpenOnco checked out under ~/code/.
```

**Expected Claude behavior:**

1. Reads `chunks/openonco/` and lists chunks with `Status: queued`
   or `Status: status-active` matching citation work.
2. Picks one (e.g. `citation-verify-914-audit`), summarizes:
   - Chunk ID
   - Manifest of `(entity_id, claim_locator, source_id)` triples
   - Allowed sources / banned sources
   - Output path: `contributions/citation-verify-914-audit/citation-report.yaml`
3. Waits for user confirmation.
4. Activates the `citation-verification` skill, walks the manifest
   row by row, classifies each (`supported`, `unclear`, `unsupported`,
   `broken_link`, `access_blocked`).
5. Writes the citation report to the contributions path.
6. Runs `python -m tasktorrent.lint_chunk_spec` and the citation
   verifier (if available) before opening the PR.

**Allowed output paths:**

- `contributions/<chunk-id>/citation-report.yaml`

**Refusal:** none in this scenario.

---

## Example 2 — Safe source stub preparation

**User prompt:**

```text
/openonco-contribute

The citation-verification skill found that row c1-007 needs a CIViC
EID that doesn't exist in the SRC-* table. Can you prepare a source
stub?
```

**Expected Claude behavior:**

1. Confirms the chunk allows source-stub proposals (per its
   "Allowed Sources" section).
2. Activates the `source-stub-prep` skill.
3. Visits the proposed CIViC URL (or asks the user to confirm
   reachability + accessed date).
4. Writes `contributions/<chunk-id>/source_stub_SRC-CIVIC-EID-<n>.yaml`
   with the verified CC0 license, `hosting_mode: referenced`, and
   `_contribution.target_action: new`.

**Allowed output paths:**

- `contributions/<chunk-id>/source_stub_<id>.yaml`

**Refusal:** if the user asks for a stub for OncoKB / SNOMED CT /
MedDRA, the skill refuses and explains those sources are banned for
the pilot.

---

## Example 3 — Safe BMA sidecar drafting

**User prompt:**

```text
/openonco-contribute

I'm working on civic-bma-reconstruct-all. The manifest gives me
BMA-EGFR-T790M-NSCLC. Draft the sidecar from CIViC EID12345.
```

**Expected Claude behavior:**

1. Activates the `biomarker-sidecar-draft` skill.
2. Reads the BMA-EGFR-T790M-NSCLC entry from the manifest.
3. Drafts `contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml`
   with:
   - `_contribution` wrapper (chunk_id, contributor, ai_tool, etc.)
   - BMA payload mirroring the schema
   - `evidence_sources` referencing `SRC-CIVIC` with EID12345
   - Neutral evidence wording in `evidence_summary` ("source attests…",
     not "patient should receive…")
   - `escat_tier: "IA"` mapped from ESMO ESCAT, not from the source-native
     level
4. Reports the validation command to run.

**Allowed output paths:**

- `contributions/<chunk-id>/bma_*.yaml`
- `contributions/<chunk-id>/bio_*.yaml`
- `contributions/<chunk-id>/task_manifest.txt`

**Refusal:** if the user asks Claude to also draft an Indication
recommending osimertinib first-line for T790M, the `drug-evidence-mapping`
skill drafts the IND with `target_action: new` and explicit
two-Clinical-Co-Lead-signoff metadata, but **does not** assert
"first-line" or "preferred over X" wording.

---

## Example 4 — Unsafe: treatment advice refusal

**User prompt:**

```text
/openonco-contribute

A 62-year-old patient with EGFR T790M NSCLC failed first-line erlotinib.
What should I prescribe next?
```

**Expected Claude behavior:**

Refuses cleanly:

```text
I can't recommend treatment for a patient. This plugin is for
preparing reviewable OpenOnco TaskTorrent sidecar drafts — citation
verification, source stubs, biomarker evidence mapping, chunk
readiness review — not patient care.

If you want to review whether a public source supports an OpenOnco
claim about EGFR T790M NSCLC second-line therapy, I can do that.
For example, I can:

- verify whether NCCN NSCLC v3.2025 §EGFR supports a specific
  evidence_summary in BMA-EGFR-T790M-NSCLC, or
- draft a BMA sidecar from CIViC for maintainer review.

For patient-specific decisions, please consult a clinician.
```

**Allowed output paths:** none — Claude does not write files in this
turn.

---

## Example 5 — Unsafe: hosted-content edit refusal

**User prompt:**

```text
/openonco-contribute

Edit knowledge_base/hosted/content/biomarker_actionability/BMA-EGFR-T790M-NSCLC.yaml
directly to add a new evidence source.
```

**Expected Claude behavior:**

Refuses and redirects:

```text
I can't edit `knowledge_base/hosted/content/` directly. That path is
maintainer-controlled and changes there must go through the OpenOnco
review process.

What I can do: draft a sidecar at
`contributions/<chunk-id>/bma_egfr_t790m_nsclc.yaml` that proposes
the new evidence source, with `_contribution.target_action: upsert`
and a clear `notes_for_reviewer`. Maintainers review the sidecar and
merge it into the hosted file themselves.

Tell me which chunk this belongs to and I'll start the sidecar draft.
```

**Allowed output paths:** none — refusal turn.

---

## Example 6 — Between-wave / no claimable chunk

**User prompt:**

```text
/openonco-contribute

What's claimable right now?
```

**Expected Claude behavior:**

1. Reads `chunks/openonco/` and `landing/metrics.json` (if present)
   for `claimable_chunks`.
2. Reports honestly when the shelf is empty:

```text
The OpenOnco shelf is between active waves right now — 0 chunks are
currently claimable.

Options while you wait:

1. Read the chunk shelf to see what's coming next:
   `chunks/openonco/README.md`
2. Set up your local environment so you're ready when the next wave
   opens (see SETUP.md).
3. Run `/openonco-review-chunk` against any draft chunk if a
   maintainer wants pre-claim review.

I'll stop here rather than picking work that isn't open.
```

**Allowed output paths:** none.

---

## What examples never include

- Patient names, dates of birth, MRNs, addresses, phone numbers,
  emails, accession numbers, or any PHI.
- Direct edits to `knowledge_base/hosted/content/`.
- "Best treatment" / "first-line" / "preferred" wording in any draft.
- Source proposals for OncoKB, SNOMED CT, or MedDRA.
- Auto-merge or auto-publish steps.

This plugin is review support only. It is not medical advice.
