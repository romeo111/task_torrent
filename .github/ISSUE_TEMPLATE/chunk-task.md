---
name: Chunk Task
about: Define one executable chunk from a Drop Pack
title: "[Chunk] "
labels: ["chunk-task", "needs-contributor"]
assignees: ""
---

## Parent Pack

<!-- e.g. openonco-civic-bma-reconstruction-1drop -->

## Chunk ID

<!-- e.g. openonco-civic-bma-reconstruction-c1 -->

## Objective


## Drop Estimate


## Required Skill


## Branch Naming Convention

<!-- For OpenOnco: tasktorrent/<pack-id>/<chunk-id> -->

## Sidecar Output Path

<!-- All output goes here. PRs touching files outside this path are auto-rejected. -->

```
contributions/<pack-id>/<chunk-id>/
```

## Chunk Manifest

<!-- Explicit list of stable entity IDs (or filename ranges) this chunk owns.
     The contributor must ALSO commit this manifest as
     contributions/<pack-id>/<chunk-id>/chunk_manifest.txt. -->

```
<entity_id_1>
<entity_id_2>
...
```

## Allowed Sources

<!-- Pull from docs/openonco-pilot-workflow.md §"Source allowlist". List the
     SRC-* IDs or source domains the chunk may reference. -->

## Disallowed Sources

<!-- Always include OncoKB, SNOMED CT, MedDRA for OpenOnco packs. -->

## Input Context

<!-- Pointers the contributor needs: existing entity files to read, the schema
     file, the relevant skill spec, the relevant audit report. -->

- Schema: `knowledge_base/schemas/<entity>.py`
- Skill spec: `skills/<skill>.md`
- Pilot workflow: `docs/openonco-pilot-workflow.md`

## AI tool + model metadata (required on every sidecar)

Each sidecar's `_contribution` wrapper must include `ai_tool` (e.g. `codex`)
and `ai_model` (e.g. `gpt-5-mini`). This is captured for audit and
regression-triage; it does not affect accept/reject. See
`docs/openonco-pilot-workflow.md` §"AI tool + model metadata" for details.

## Output Format

<!-- One YAML file per entity in the manifest, using the schema's wrapper +
     payload shape. See the skill spec for the exact template. -->

## Acceptance Criteria (machine-checkable)

- [ ] Every sidecar has `_contribution.ai_tool` and `_contribution.ai_model` set.
- [ ] PR branch name matches `tasktorrent/<pack-id>/<chunk-id>`.
- [ ] `git diff --name-only main..HEAD` lists only files under `contributions/<pack-id>/<chunk-id>/`.
- [ ] `chunk_manifest.txt` is committed and matches the manifest in this issue.
- [ ] Every sidecar's `_contribution.target_entity_id` is in the chunk manifest.
- [ ] Every sidecar passes Pydantic validation (after `_contribution:` strip).
- [ ] `pytest tests/` passes on the contributor branch.
- [ ] Every `_contribution.target_action: upsert` references an entity that exists on `main`.
- [ ] Every `_contribution.target_action: new` does NOT collide with an existing ID on `main`.
- [ ] Every `SRC-*` referenced exists on `main` OR has a `source_stub_*.yaml` in the chunk directory.
- [ ] No banned source (`SRC-ONCOKB`, etc.) appears in contributor-authored output.

## Acceptance Criteria (semantic, maintainer-checked)

- [ ] Output stays inside assigned chunk manifest.
- [ ] Required schema is followed (no invented fields).
- [ ] Stable IDs preserved for `target_action: upsert`.
- [ ] Duplicates flagged with `target_action: flag_duplicate` and `duplicate_of: <stable-id>`.
- [ ] Maintainer can review the output without private context.

## Rejection Criteria

- Medical advice
- Treatment recommendation wording
- Patient-specific output
- Missing or fake citations
- Banned source used (e.g. `SRC-ONCOKB`)
- Unrelated edits or files outside sidecar path
- Entity IDs outside the chunk manifest
- Pre-commit hooks bypassed (`--no-verify`)
- `git add -A` / `git add .` evidence (untracked files swept in)
