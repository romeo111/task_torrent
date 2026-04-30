# OpenOnco Contributor Plugin Plan

## Status

Planning document for a public Claude plugin submission.

Target plugin:

```text
plugins/openonco-contributor/
```

Plugin name (manifest `name` field):

```text
openonco-contributor
```

Initial version: `0.4.0` (matches the TaskTorrent v0.4 protocol the plugin targets).

## Goal

Create a public, directory-ready Claude plugin that lets contributors donate
AI-agent time to OpenOnco by completing one reviewable TaskTorrent chunk at a
time.

The plugin should help with research and data-preparation work only. It must
produce sidecar drafts, citation reports, source stubs, and review checklists
for OpenOnco maintainers. It must not provide medical advice, patient-specific
recommendations, autonomous publication, autonomous merge, or direct edits to
hosted clinical content.

## Why This Plugin Should Exist

OpenOnco has structured oncology data work that is useful, bounded, and
review-heavy:

- citation verification
- source metadata cleanup
- biomarker evidence reconstruction
- sidecar formatting
- manifest consistency checks
- schema-aware pre-review

Those tasks are a good fit for contributor agents because they can be scoped as
one chunk, one manifest, one branch, one PR, and one maintainer review. The
plugin packages that workflow for Claude users without requiring them to read
the full TaskTorrent protocol first.

## Submission Strategy

Do not submit the repo root.

Submit a narrow plugin subdirectory:

```text
plugins/openonco-contributor/
```

Reasons:

- Anthropic plugin validation expects plugin metadata and components in a
  plugin directory.
- The repo root includes docs, generated landing data, a Python package,
  shell bootstrap scripts, chunk specs, and protocol history. That is too broad
  for a clean directory artifact.
- A narrow plugin can have a precise safety boundary and a small permission
  surface.

## Directory Layout

```text
.claude-plugin/
  marketplace.json                          # repo-root marketplace listing
plugins/openonco-contributor/
  .claude-plugin/
    plugin.json
  skills/
    citation-verification/
      SKILL.md                              # migrated from skills/citation-verification.md
    biomarker-sidecar-draft/
      SKILL.md                              # migrated+renamed from skills/biomarker-extraction.md
    drug-evidence-mapping/
      SKILL.md                              # migrated from skills/drug-evidence-mapping.md
    source-stub-prep/
      SKILL.md                              # net-new; format extracted from citation-verification
    chunk-readiness-review/
      SKILL.md                              # net-new; sources its checks from tasktorrent/lint_chunk_spec.py
  commands/
    openonco-contribute.md
    openonco-review-chunk.md
  SETUP.md
  EXAMPLES.md
  PRIVACY.md
  SECURITY.md
  SUPPORT.md
  LICENSE                                   # MIT, copied from repo root
  README.md
```

No MCP server is needed for v1. No hooks are needed for v1. No installer script
should be exposed as the primary plugin path.

The repo also requires a top-level `LICENSE` file (MIT) — none currently exists.
Add it before submission.

## Dependency Strategy

The v1 contributor plugin should have no plugin dependencies.

Reason:

- Fewer dependencies make Anthropic directory review simpler.
- The plugin can bundle all behavior-critical instructions locally.
- There is no shared MCP server or shared safety plugin that must be installed
  for v1.

If later versions split shared safety rules, OpenOnco schemas, or TaskTorrent
utilities into separate Claude plugins, dependency versions must be constrained
in `.claude-plugin/plugin.json`. Claude Code resolves plugin dependencies
automatically, and unconstrained dependencies track the latest available
version. That is risky for high-stakes contribution workflows because an
upstream plugin can change behavior without warning.

Use explicit semver ranges:

```json
{
  "name": "openonco-contributor",
  "version": "0.5.0",
  "dependencies": [
    { "name": "tasktorrent-core", "version": "~0.4.0" },
    { "name": "openonco-source-policy", "version": "~0.4.0" }
  ]
}
```

These dependency plugins (`tasktorrent-core`, `openonco-source-policy`) do not
exist today. They are aspirational v2+ split points, listed here only to fix
the policy when/if shared plugins ever ship. v1 has no plugin dependencies.

Rules:

1. Prefer no dependencies in v1.
2. If dependencies are introduced, pin them with `~` ranges until integration
   tests prove a wider range is safe.
3. Do not use cross-marketplace dependencies unless the root marketplace
   explicitly allowlists the target marketplace.
4. Tag every plugin release with Claude's required convention:
   `{plugin-name}--v{version}`.
5. Use `claude plugin tag --push` for releases when possible.
6. Before widening a dependency range, run the OpenOnco unsafe-prompt tests and
   chunk workflow tests.
7. Document dependency errors and recovery in `SETUP.md`, including
   `claude plugin list --json`, `/doctor`, `/plugin`, and `claude plugin prune`.

Release gates once dependencies exist:

```bash
claude plugin validate plugins/openonco-contributor
claude plugin tag --dry-run
claude plugin list --json
```

## Marketplace Listing

For users to install the plugin via `/plugin install openonco-contributor@<repo>`,
the repo needs a marketplace file at `.claude-plugin/marketplace.json` (repo
root, not plugin root):

```json
{
  "name": "tasktorrent",
  "owner": { "name": "TaskTorrent contributors", "url": "https://github.com/romeo111/task_torrent" },
  "plugins": [
    {
      "name": "openonco-contributor",
      "source": "./plugins/openonco-contributor",
      "description": "OpenOnco TaskTorrent contributor — sidecar drafts, citation verification, chunk readiness review. Not medical advice."
    }
  ]
}
```

When the clinical-review plugin is added later, it lands as a second entry in
the same `plugins[]` array.

## Migration From Repo-Level Skills

Today the repo has three skill files at `skills/` that the existing
README contributor prompt loads via plain markdown:

| Existing path | Action | New path |
|---|---|---|
| `skills/citation-verification.md` | move | `plugins/openonco-contributor/skills/citation-verification/SKILL.md` |
| `skills/biomarker-extraction.md` | move + rename | `plugins/openonco-contributor/skills/biomarker-sidecar-draft/SKILL.md` |
| `skills/drug-evidence-mapping.md` | move | `plugins/openonco-contributor/skills/drug-evidence-mapping/SKILL.md` |

Migration rules:

1. The plugin version becomes the canonical copy. Repo-level files are
   removed in the same commit.
2. README's "Contribute To Cancer Research" prompt links to plugin install
   instead of pasting raw skill content.
3. SKILL.md frontmatter (YAML) is added on migration:
   ```yaml
   ---
   name: <skill-name>
   description: <one-line trigger description>
   ---
   ```
4. Body content is preserved verbatim except for path-relative links.

## Plugin Manifest

Draft `plugins/openonco-contributor/.claude-plugin/plugin.json`:

```json
{
  "name": "openonco-contributor",
  "version": "0.4.0",
  "description": "Prepare reviewable OpenOnco TaskTorrent sidecar drafts for citation verification, source stubs, biomarker and drug evidence mapping, and chunk readiness review. Not medical advice. Does not edit hosted clinical content or process PHI.",
  "author": {
    "name": "TaskTorrent contributors",
    "url": "https://github.com/romeo111/task_torrent"
  },
  "homepage": "https://github.com/romeo111/task_torrent",
  "repository": "https://github.com/romeo111/task_torrent",
  "license": "MIT",
  "keywords": [
    "openonco",
    "tasktorrent",
    "oncology",
    "citation-verification",
    "evidence-review",
    "open-source"
  ]
}
```

Initial release is `0.4.0` to match the TaskTorrent v0.4 protocol the plugin
targets. Bump to `0.5.0` when the protocol bumps; bump to `1.0.0` only after
the plugin has been listed publicly and observed in real contributor use for
at least one wave.

The literal phrase **"Not medical advice"** appears in the description so it
is visible in any directory listing without expanding the plugin card.

## Core Safety Contract

Every skill and command must include the same hard boundary:

1. Work on exactly one chunk.
2. Stay inside `contributions/<chunk-id>/` unless the chunk explicitly permits
   another path.
3. Produce drafts for maintainer review.
4. Do not edit `knowledge_base/hosted/content/`.
5. Do not write treatment advice.
6. Do not write patient-specific output.
7. Do not use banned sources.
8. Do not claim clinical correctness.
9. Do not bypass validation.
10. Stop after opening or preparing one PR.

## Allowed Workflows

### Citation Verification

Purpose:

- Verify whether cited public sources support specific OpenOnco claims.
- Produce a structured report for maintainers.

Allowed outputs:

- `contributions/<chunk-id>/citation-report.yaml`
- optional `source_stub_*.yaml` when the chunk allows source stub proposals

Disallowed outputs:

- direct edits to clinical content
- rewritten recommendations
- replacement of maintainer judgment

### Source Stub Preparation

Purpose:

- Prepare metadata for sources that maintainers may ingest later.
- Capture URL, title, access level, license, provenance, and related IDs.

Allowed outputs:

- `contributions/<chunk-id>/source_stub_<source-id>.yaml`

The source stub YAML schema is the one already documented in
`skills/citation-verification.md` §"Source Stub" (extracted into the new
`source-stub-prep` skill on migration). License classification is a
review gate, not a formality (see `SOURCE_INGESTION_SPEC.md` §8/§20 in the
consumer repo).

Required checks:

- source is real and reachable
- license/access fields are not guessed
- source is allowed for the chunk
- banned sources are not proposed

### Drug & Indication Sidecar Drafting

Purpose:

- Draft `Drug` (DRUG-*) and `Indication` (IND-*) entity sidecars with full
  provenance, neutral wording, and explicit two-Clinical-Co-Lead signoff
  metadata.

Allowed outputs:

- `contributions/<chunk-id>/drug_<drug>.yaml`
- `contributions/<chunk-id>/ind_<indication>.yaml`
- `contributions/<chunk-id>/task_manifest.txt`

Required constraints:

- one entity per file
- every target entity is in the manifest
- every claim traces to allowed sources
- neutral evidence wording only
- no treatment recommendation language
- claim-bearing fields require `requires_clinical_co_lead_signoff: true`

### Biomarker Sidecar Drafting

Purpose:

- Draft BiomarkerActionability or Biomarker sidecar candidates for maintainer
  review.

Allowed outputs:

- `contributions/<chunk-id>/bma_*.yaml`
- `contributions/<chunk-id>/bio_*.yaml`
- `contributions/<chunk-id>/task_manifest.txt`

Required constraints:

- one entity per file
- every target entity is in the manifest
- every claim traces to allowed sources
- neutral evidence wording only
- no treatment recommendation language

### Chunk Readiness Review

Purpose:

- Help maintainers and contributors determine whether a chunk is ready to open
  or claim.

Allowed outputs:

- review notes
- manifest warnings
- missing section checklist
- source policy checklist
- linter command recommendations

Disallowed outputs:

- opening issues automatically unless the user explicitly asks
- modifying chunk specs without explicit user request

## Explicit Non-Goals

The plugin must not:

- provide medical advice
- answer patient-specific questions
- choose treatment
- rank treatment options
- decide dosing
- interpret patient records
- process PHI
- auto-merge PRs
- publish hosted clinical content
- run broad install scripts without explicit user approval
- collect analytics
- send data to non-Claude/non-GitHub services

## Skill Design

### `citation-verification/SKILL.md`

Trigger:

- user asks to verify citations
- user is working on an OpenOnco citation chunk
- user has a manifest of claim/source pairs

Core behavior:

- read the chunk spec and local files supplied by the user
- list manifest rows before work
- verify each row against allowed source text available to the user
- classify support as `supported`, `unclear`, `unsupported`,
  `broken_link`, or `access_blocked`
- output a structured report
- never edit clinical content

Quality gates:

- each row has an accessed date
- each row has a concrete source locator where possible
- `supported` requires direct support, not topic adjacency
- uncertainty defaults to maintainer review

### `source-stub-prep/SKILL.md`

Trigger:

- user asks to prepare source metadata
- citation verification finds a missing source
- chunk explicitly permits source stubs

Core behavior:

- produce source stubs only for allowed sources
- capture license/access uncertainty honestly
- refuse source stubs for banned sources
- flag paywalled/restricted access instead of guessing

Quality gates:

- URL resolves or is marked unresolved
- license fields are sourced
- stable source ID convention is followed

### `biomarker-sidecar-draft/SKILL.md`

Trigger:

- user asks to draft BMA/BIO sidecars
- chunk manifest includes BMA/BIO entities

Core behavior:

- draft only manifest-owned entities
- use neutral evidence language
- cite existing `SRC-*` IDs or permitted source stubs
- preserve schema shape
- include `_contribution` metadata

Quality gates:

- no recommendation wording
- no invented entity IDs outside the manifest
- no free-text URLs in source fields where `SRC-*` IDs are required
- validation command is reported

### `drug-evidence-mapping/SKILL.md`

Trigger:

- user asks to draft DRUG-* / IND-* sidecars
- chunk manifest includes drug or indication entities
- user is on a regimen-outcome-fill, drug-class-normalization, or
  redflag-indication-coverage-fill chunk

Core behavior:

- draft only manifest-owned entities
- preserve schema shape (`knowledge_base/schemas/drug.py`,
  `knowledge_base/schemas/indication.py`)
- use neutral evidence language
- cite existing `SRC-*` IDs or permitted source stubs
- mark every claim-bearing field with `requires_clinical_co_lead_signoff: true`
- include `_contribution` metadata

Quality gates:

- no recommendation wording (no "preferred", "first-line", "should")
- no invented entity IDs outside the manifest
- no free-text URLs in source fields where `SRC-*` IDs are required
- two-Clinical-Co-Lead signoff gate present on every claim-bearing field

### `chunk-readiness-review/SKILL.md`

Trigger:

- user asks whether a chunk is ready to open or claim
- user asks to review a chunk spec

Core behavior:

- compare chunk to TaskTorrent v0.4 required sections — source of truth is
  `tasktorrent/lint_chunk_spec.py` `REQUIRED_SECTIONS` and the linter's
  validation behavior, not a hand-maintained list
- check source policy
- check manifest concreteness
- check sidecar output path
- check claim method and Drop estimate
- recommend fixes before the issue opens

Quality gates:

- no false assurance
- concrete file/section references
- separate blocking issues from warnings

## Commands

### `/openonco-contribute`

Purpose:

Guide a contributor through one OpenOnco TaskTorrent chunk.

Prompt skeleton:

```text
Help me contribute one OpenOnco TaskTorrent chunk.

Use only local files and user-provided GitHub context unless I explicitly ask
you to fetch current GitHub issue state. Pick one claimable chunk, summarize its
scope, confirm allowed and banned sources, work only under
contributions/<chunk-id>/, run validation, prepare one PR, then stop.

Do not produce medical advice, patient-specific output, or direct hosted
clinical-content edits.
```

### `/openonco-review-chunk`

Purpose:

Review a chunk spec or issue body before a contributor starts.

Output:

- blocking issues
- warnings
- source policy notes
- manifest notes
- validation plan

## SETUP.md Requirements

`SETUP.md` should be short and explicit:

- no remote MCP server
- no plugin-owned data collection
- GitHub CLI is optional and only needed if the user wants Claude to inspect
  or prepare PR work
- user must be in a local OpenOnco checkout for file edits
- user must not paste PHI
- users should run validation before PR

It should not tell users to run `curl | bash`.

## PRIVACY.md Requirements

State:

- plugin itself does not collect analytics
- plugin itself does not run a backend
- plugin processes local repo files and user-provided content inside Claude
- user controls GitHub interactions
- PHI is prohibited
- do not paste patient records or identifiers
- support/security contact location

## SECURITY.md Requirements

State:

- report vulnerabilities through GitHub issues or a named contact channel
- do not include secrets, tokens, PHI, or private patient data in reports
- plugin does not require API keys beyond user-managed tools
- no auto-merge or direct publish capability

## SUPPORT.md Requirements

State:

- where to ask usage questions
- where to report broken plugin behavior
- expected response model
- what is not supportable, including medical advice requests

## EXAMPLES.md Requirements

Anthropic policy asks for at least three working examples or use cases.

Include:

1. Safe citation verification.
2. Safe source stub preparation.
3. Safe BMA sidecar drafting.
4. Unsafe treatment advice refusal.
5. Unsafe PHI refusal.

Each example should include:

- user prompt
- expected Claude behavior
- allowed output paths
- refusal or safety note when relevant

## Validation Plan

Before submission:

```bash
claude plugin validate plugins/openonco-contributor
```

Manual tests:

1. Start Claude Code with the plugin installed locally.
2. Confirm `/openonco-contribute` appears.
3. Confirm skills are discovered.
4. Ask for citation verification.
5. Ask for BMA sidecar drafting.
6. Ask for patient-specific treatment advice and verify refusal.
7. Ask to edit `knowledge_base/hosted/content/` and verify refusal unless the
   user explicitly changes scope outside the plugin's normal workflow.

Repo tests:

```bash
python -m tasktorrent.lint_chunk_spec --all chunks/openonco/
python -m pytest tests/test_lint_chunk_spec.py::test_lint_real_openonco_chunks_pass_without_warnings tests/test_openonco_job.py -q
```

## Anthropic Policy Alignment Checklist

Submission docs:

- public GitHub repo or zip
- `claude plugin validate` passes
- plugin is submitted through Anthropic form

Software Directory Policy:

- no safety bypass
- no hidden instructions
- no dynamic behavioral instructions from external sources
- narrow, unambiguous descriptions
- no extraneous data collection
- no IP-infringing content
- support and security channels documented
- at least three examples

Software Directory Terms:

- rights and license are clear
- docs are accurate
- privacy docs are present if user data is processed
- vulnerability reporting mechanism exists

## Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| Plugin appears to provide medical advice | High | Description and every skill says draft/review support only. Add refusal examples. |
| Claude edits hosted clinical content | High | Skills restrict output to `contributions/<chunk-id>/`. |
| Contributor uses banned sources | High | Bundle banned-source rules and source policy checks. |
| Dynamic GitHub docs become behavioral source | Medium | Bundle core behavior in plugin. External links are references only. |
| Installer looks unsafe | Medium | Do not expose `landing/install.sh` as plugin setup path. |
| No claimable chunks | Low | Plugin reports between-wave state and stops. |
| Validation drift | Medium | Add local `claude plugin validate` to release checklist. |

## Release Criteria

The contributor plugin is ready to submit when:

- `claude plugin validate plugins/openonco-contributor` passes
- all plugin skills are in `skills/<name>/SKILL.md`
- all behavior-critical instructions are bundled locally
- privacy/security/support docs exist
- examples cover safe and unsafe requests
- no MCP server or shell installer is needed
- no plugin dependencies exist, or every dependency has a tested semver range
- README clearly says this is not medical advice
- OpenOnco linter gate passes

## First Implementation Slice

Concrete file-by-file work order:

1. Add `LICENSE` (MIT) at repo root.
2. Add `.claude-plugin/marketplace.json` at repo root.
3. Create `plugins/openonco-contributor/.claude-plugin/plugin.json`
   with `name=openonco-contributor`, `version=0.4.0`, MIT license,
   description containing "Not medical advice".
4. Migrate three existing skills into plugin structure:
   - `skills/citation-verification.md` →
     `plugins/openonco-contributor/skills/citation-verification/SKILL.md`
   - `skills/biomarker-extraction.md` (renamed) →
     `plugins/openonco-contributor/skills/biomarker-sidecar-draft/SKILL.md`
   - `skills/drug-evidence-mapping.md` →
     `plugins/openonco-contributor/skills/drug-evidence-mapping/SKILL.md`
   Add YAML frontmatter (`name`, `description`) on each.
   Delete the originals at `skills/`.
5. Create `plugins/openonco-contributor/skills/source-stub-prep/SKILL.md`
   (extract source stub schema from current `skills/citation-verification.md`).
6. Create `plugins/openonco-contributor/skills/chunk-readiness-review/SKILL.md`
   sourcing checks from `tasktorrent/lint_chunk_spec.py`.
7. Create command files:
   - `plugins/openonco-contributor/commands/openonco-contribute.md`
   - `plugins/openonco-contributor/commands/openonco-review-chunk.md`
   Both with frontmatter `description:` and `user-invocable: true`.
8. Create plugin docs:
   - `plugins/openonco-contributor/SETUP.md`
   - `plugins/openonco-contributor/EXAMPLES.md` (≥3 safe + ≥2 unsafe + 1
     between-wave example)
   - `plugins/openonco-contributor/PRIVACY.md`
   - `plugins/openonco-contributor/SECURITY.md`
   - `plugins/openonco-contributor/SUPPORT.md`
   - `plugins/openonco-contributor/README.md`
   - `plugins/openonco-contributor/LICENSE` (copy of repo-root MIT)
9. Update repo `README.md` "How to contribute" section to point at the
   plugin install path instead of pasting raw skill content.
10. Run `claude plugin validate plugins/openonco-contributor`.
11. Run repo tests:
    - `python -m tasktorrent.lint_chunk_spec --all chunks/openonco/`
    - `python -m pytest tests/test_lint_chunk_spec.py tests/test_openonco_job.py -q`
12. Iterate until validation and tests pass.
