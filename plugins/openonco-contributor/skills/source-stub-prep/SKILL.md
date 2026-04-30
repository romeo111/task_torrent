---
name: source-stub-prep
description: Prepare a `source_stub_<source-id>.yaml` describing a real, accessible source so OpenOnco maintainers can decide whether to ingest it as a new `Source` (SRC-*) entity. Use when citation verification finds a missing source, or when a chunk explicitly permits source stubs. Drafts only — refuses banned sources, marks paywall/access-blocked honestly, never invents license/access fields.
---

# Skill: Source Stub Preparation

## Purpose

Capture metadata for sources that maintainers may ingest later as new `Source` (SRC-*) entities in OpenOnco. This skill produces a stub for review — it does not register a source or merge anything into hosted clinical content.

## When To Use

Use this skill when:

- citation verification finds a claim that is supportable but no existing `SRC-*` entry covers the cited source, and
- the chunk's "Allowed Sources" section permits source-stub proposals, and
- the source is real, reachable, and not on the banned list.

Do not use this skill when:

- the chunk does not authorize source stubs
- the source is paywalled or geo-restricted (mark `support_status: access_blocked` in the citation report instead)
- the source is on the banned list (OncoKB, SNOMED CT, MedDRA — see `docs/openonco-pilot-workflow.md`)

## Allowed Output

One file per proposed source:

```text
contributions/<chunk-id>/source_stub_<proposed_id>.yaml
```

Maintainers ingest source stubs through the `SOURCE_INGESTION_SPEC.md` §8/§20 review flow in the consumer repo. License classification is a **gate**, not a formality.

## Output Schema

The stub mirrors the real `Source` entity schema (`knowledge_base/schemas/source.py`) plus a `_contribution` wrapper that maintainers strip on merge:

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

## Stable ID Conventions

Use the source-family prefix that matches the publisher:

| Family | Example ID format |
|---|---|
| CIViC | `SRC-CIVIC-EID-<eid>` (per evidence item) or `SRC-CIVIC` (whole DB) |
| PubMed | `SRC-PMID-<pmid>` |
| PubMed Central OA | `SRC-PMC-<pmcid>` |
| DailyMed | `SRC-DAILYMED-<drug-or-spl-id>` |
| openFDA | `SRC-OPENFDA-<context>` |
| ClinicalTrials.gov | `SRC-CT-<NCT-id>` |
| ESMO | `SRC-ESMO-<topic-or-version>` |
| ASCO | `SRC-ASCO-<topic>` |
| NCCN | `SRC-NCCN-<DISEASE>-<VERSION>` |
| WHO Classification | `SRC-WHO-<classification>` |
| МОЗ України | `SRC-MOZ-<order-id>` |

Match neighbouring `SRC-*` IDs in `chunks/openonco/source-stub-ingest-batch.md` and existing source files when in doubt.

## License & Access Rules

- Copy `license.spdx_id` verbatim from the publisher (e.g. CIViC → `CC0-1.0`, PubMed Central OA → varies per article — use the article's CC license, not "PubMed").
- Set `access_level` honestly: `open_access`, `restricted_redistribution`, `paywalled`, `geo_restricted`.
- For NCCN / WHO / ESMO: set `hosting_mode: referenced`. Do not assert `redistribution_allowed: true` unless the publisher explicitly grants it.
- If you cannot find the license, do not guess. Set `license: null` and add `_contribution.notes_for_reviewer: "License unverified at <accessed date>; needs maintainer license review."`

## Banned Sources — Refuse

Do not file source stubs for:

- **OncoKB** — ToS conflicts with the OpenOnco CHARTER §2 free-public, non-commercial requirement.
- **SNOMED CT** — license-gated.
- **MedDRA** — license-gated.

If the chunk lists one of these as an "Allowed Source," that is a chunk-spec error. Stop and surface the conflict in the citation report's `notes_for_reviewer`.

## Rules

- The proposed source must be real, reachable, and accessed by you (or the user) on the recorded `last_verified` date.
- Do not propose a stub for a source you have not actually visited.
- Do not invent `license`, `commercial_use_allowed`, `redistribution_allowed`, or `modifications_allowed` — these are review gates.
- One stub per file. No multi-source batch files.
- Do not link a stub directly into hosted clinical content. Stubs are review-only.

## Good Output

A stub that:

- Names a real, dated, reachable URL.
- Carries a verifiable SPDX license tag from the publisher.
- Uses a stable `SRC-*` ID convention matching neighbours.
- Sets `_contribution.target_action: new` and explains the dependency in `notes_for_reviewer`.

## Bad Output

- A stub with `license: null` and `commercial_use_allowed: true` (license unknown but rights asserted).
- A stub for OncoKB / SNOMED CT / MedDRA.
- A stub with `url:` that does not resolve.
- A stub without `last_verified` date.
- A stub proposing a license guess based on the source family rather than the actual publisher terms.
