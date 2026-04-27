## Pack

<!-- e.g. openonco-civic-bma-reconstruction-1drop -->

## Chunk

<!-- e.g. openonco-civic-bma-reconstruction-c1 -->

## Linked Chunk Issue

<!-- Closes #<issue-number> -->

## What Was Completed

<!-- One paragraph. What entity IDs did you draft / verify / report on? -->

## AI Tool Used

- [ ] Claude Code
- [ ] Codex
- [ ] Cursor
- [ ] ChatGPT
- [ ] Other:

## Output Type

- [ ] BMA sidecar(s) under `contributions/<pack>/<chunk>/`
- [ ] Biomarker (BIO-*) sidecar(s)
- [ ] Drug (DRUG-*) sidecar(s)
- [ ] Indication (IND-*) sidecar(s)
- [ ] Source stub(s) (`source_stub_*.yaml`)
- [ ] Citation report (`citation-report.yaml`)
- [ ] Other:

## Sources Used

<!-- List the SRC-* IDs you cited. Confirm none are on the banned list. -->

## Safety Checklist

- [ ] No medical advice anywhere in the output
- [ ] No treatment recommendation wording (no "best", "preferred", "patients should")
- [ ] No patient-specific outputs
- [ ] Every clinical claim cites a `SRC-*` ID (not a raw URL)
- [ ] No fake citations or invented `SRC-*` IDs
- [ ] No banned sources (`SRC-ONCOKB`, SNOMED CT, MedDRA)
- [ ] AI-generated output is marked `_contribution.*` for maintainer review

## Machine-Checkable Validation

- [ ] Branch name matches `tasktorrent/<pack-id>/<chunk-id>`
- [ ] `git diff --name-only main..HEAD` lists only `contributions/<pack-id>/<chunk-id>/...` files
- [ ] `chunk_manifest.txt` committed and matches the chunk issue's manifest
- [ ] All `_contribution.target_entity_id` values are in the chunk manifest
- [ ] All sidecars pass Pydantic validation (after `_contribution:` strip)
- [ ] `pytest tests/` passes on this branch
- [ ] All `target_action: upsert` references existing entities on `main`
- [ ] All `target_action: new` does NOT collide with existing IDs on `main`
- [ ] All `SRC-*` references exist on `main` OR have a `source_stub_*.yaml` in the chunk directory
- [ ] No `--no-verify` used; pre-commit hooks ran
- [ ] No `git add -A` / `git add .` (only explicit pathspecs)

## Semantic Validation

- [ ] Output stays inside assigned chunk manifest
- [ ] Schema followed exactly (no invented fields)
- [ ] Stable IDs preserved for upsert actions
- [ ] Duplicates flagged with `target_action: flag_duplicate` + `duplicate_of:`
- [ ] Unsupported / unclear claims explicitly marked (`actionability_review_required: true` or `support_status: unclear`)
- [ ] `_contribution.notes_for_reviewer` explains any non-obvious choice

## Reviewer Notes
