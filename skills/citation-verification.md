# Skill: Citation Verification

## Purpose

For each (claim, source) pair listed in a chunk manifest, verify whether the cited source supports the claim, and emit a structured row maintainers can act on. This skill produces **review reports**, not edits to clinical content.

## Project Context

In OpenOnco, every citation is an entry in the `Source` entity table (`SRC-*` stable IDs, schema `knowledge_base/schemas/source.py`). Clinical content (Indication, BMA, Drug, RedFlag, etc.) cites sources by `SRC-*` ID, not by raw URL. The repo includes a recent audit — `docs/reviews/citation-verification-2026-04-27.md` — listing 914 findings across 464 entities; that report is the seed corpus for the pilot citation-verification pack.

## Input

The chunk issue gives you:

- **Chunk ID**
- **Chunk manifest** — explicit list of `(entity_id, claim_locator, source_id)` triples to check, with row counts. Format:
  ```
  entity_id: BMA-EGFR-T790M-NSCLC
  claim_locator: evidence_summary
  source_id: SRC-NCCN-NSCLC-2025
  source_section: "EGFR — Subsequent Therapy"
  ```
- **Allowed source list** — `docs/openonco-pilot-workflow.md` §"Source allowlist"
- **Source access notes** — for paywalled sources, the chunk states whether abstract-only checking is acceptable.

You must not check `(entity, claim, source)` triples that are not in the manifest.

## Output Schema

Submit one report file per chunk to `contributions/<chunk-id>/citation-report.yaml`. Schema:

```yaml
_contribution:

  chunk_id: openonco-citation-verification-c1
  contributor: github-username
  submission_date: "YYYY-MM-DD"
  ai_tool: claude-code | codex | cursor | chatgpt | other
  notes_for_reviewer: ""

rows:
  - row_id: c1-001                       # contributor-assigned, unique within file
    entity_id: BMA-EGFR-T790M-NSCLC
    claim_locator: evidence_summary       # field name OR explicit excerpt range
    claim_excerpt: >
      "...standard 2L is osimertinib..."
    source_id: SRC-NCCN-NSCLC-2025
    source_section: "EGFR — Subsequent Therapy"
    source_url_checked: "https://example.org/nccn-nsclc-v3-2025"
    accessed: "YYYY-MM-DD"
    support_status: supported   # supported | unclear | unsupported | broken_link | access_blocked
    rationale: >
      The cited section explicitly names osimertinib as the preferred 2L
      agent for T790M-positive NSCLC. Direct quote located on §EGFR
      subsequent-therapy page.
    suggested_action: keep      # keep | revise_claim | replace_source | maintainer_review | source_stub_needed
    suggested_replacement_source_id: null   # only when suggested_action=replace_source AND replacement is an existing SRC-*
    notes: ""
```

`support_status` values:

- **supported** — the cited section directly attests the claim. Cite the section/page locator in `rationale`.
- **unclear** — partial / ambiguous / topic-adjacent. Default for sources that mention the area but do not directly attest the specific claim.
- **unsupported** — source explicitly does not attest, or the source contradicts the claim. Quote the relevant text in `rationale`.
- **broken_link** — URL does not resolve, source entity does not exist in the SRC-* table, or `superseded_by` points to a missing entity.
- **access_blocked** — the source is paywalled or geo-restricted and the chunk did not authorize abstract-only checking. Mark as access_blocked rather than guessing.

`suggested_action` values:

- **keep** — citation is fine; no maintainer action.
- **revise_claim** — claim wording overstates what the source attests; suggest narrower wording in `rationale`. Do not rewrite clinical content directly.
- **replace_source** — claim is supportable but the cited source does not support it; propose a different existing `SRC-*` ID in `suggested_replacement_source_id`. Do not propose a URL or a new source here.
- **maintainer_review** — uncertain or politically sensitive (controversy entries, off-label, ESCAT-borderline). Default when in doubt.
- **source_stub_needed** — claim is supportable but no existing `SRC-*` exists for the appropriate source. File a separate `source_stub.yaml` (template below).

## Source Stub (when proposing a new Source)

Submit to `contributions/<chunk-id>/source_stub_<proposed_id>.yaml`. Maintainers ingest source stubs through the separate `SOURCE_INGESTION_SPEC.md` §8/§20 review flow — license classification is a gate, not a formality.

```yaml
_contribution:

  chunk_id: <chunk>
  contributor: github-username
  target_action: new
  target_entity_id: SRC-CIVIC-EID-12345
  ai_tool: <tool>
  notes_for_reviewer: >
    Source needed by row c1-007. License: CC0 (CIViC). No hosting needed
    (HostingMode.REFERENCED).

# Source payload — fields match knowledge_base/schemas/source.py
id: SRC-CIVIC-EID-12345
source_type: molecular_kb
title: "CIViC Evidence Item EID12345"
url: "https://civicdb.org/evidence/12345"
access_level: open_access
hosting_mode: referenced
license:
  spdx_id: "CC0-1.0"
  url: "https://creativecommons.org/publicdomain/zero/1.0/"
commercial_use_allowed: true
redistribution_allowed: true
modifications_allowed: true
attribution:
  required: true
  text: "Griffith Lab — CIViC (https://civicdb.org)"
relates_to_diseases: ["DIS-NSCLC"]
notes: "Evidence Item 12345 attests EGFR T790M sensitivity to osimertinib."
last_verified: "YYYY-MM-DD"
verifier: "github-username"
```

For paywalled or restricted sources, do not file a stub speculatively — flag `support_status: access_blocked` instead and let the maintainer decide.

## Rules

- Stay inside the chunk manifest. Do not check rows outside it.
- Do not invent replacement citations. Replacement sources must be (a) an existing `SRC-*` ID, or (b) a properly filed `source_stub.yaml` for a real, accessible source.
- Topic adjacency is not support. A guideline that mentions EGFR-TKIs as a class does not "support" a claim about a specific drug at a specific line of therapy unless the section explicitly attests that combination.
- Do not rewrite claim text. `suggested_action: revise_claim` describes the suggested change in `rationale`; maintainers make the edit.
- Do not coerce non-allowed sources. If a chunk lists a banned source (e.g. `SRC-ONCOKB`), mark `support_status: access_blocked` with `notes: "OncoKB is not an allowed source for this pilot."`
- For broken links, check whether `Source.url` and `Source.superseded_by` differ. A `broken_link` rationale should distinguish "URL does not resolve" from "Source entity superseded but successor not linked."

## Good Output

A row that:

- Names the exact section / page / quote that attests the claim.
- Uses `support_status: supported` only when the source text *says* what the claim says.
- Uses `support_status: unclear` when the source is topic-adjacent.
- Includes `accessed: <date>` so a reviewer can re-verify.

## Bad Output

- `support_status: supported` with `rationale: "Probably true."`
- `suggested_action: replace_source` with a new URL in `suggested_replacement_source_id` instead of a `SRC-*` ID.
- A row checking a `(entity, claim, source)` triple not listed in the manifest.
- Rewriting the claim text inside `rationale`.
- `support_status: broken_link` without an `accessed` date or any check evidence.
