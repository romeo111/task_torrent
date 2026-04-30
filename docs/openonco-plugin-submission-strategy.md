# OpenOnco Plugin — Anthropic Directory Submission Strategy

## Status

Submission strategy for the `openonco-contributor` Claude Code plugin
(v0.4.0). Targets the Anthropic plugin directory.

## Submission paths

Anthropic verified two intake forms (per [code.claude.com/docs/en/plugins
§"Submit your plugin to the official marketplace"](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-official-marketplace)):

- Claude.ai: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- Console: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

Either form is the entry point for the **general directory**, which is
backed by [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official).

A separate **life-sciences marketplace** exists at
[`anthropics/life-sciences`](https://github.com/anthropics/life-sciences).
It hosts plugins like `biorxiv`, `chembl`, `clinical-trials`,
`10x-genomics`, `scvi-tools`, etc. The repo's README states it
"will continue to host the marketplace.json long-term, but not the
actual MCP servers." Public contribution guidelines are not
documented. Existing plugins there are predominantly MCP-server-bundled
scientific-data tools, which is not how `openonco-contributor` is
shaped today.

## Recommendation

**Submit to the general directory first** via Claude.ai or Console
form. Reasons:

- The plugin meets all general-directory documented requirements
  (MIT license, validated manifest, ≥3 examples, PRIVACY/SECURITY/SUPPORT,
  banned-source refusal in metadata).
- Submission flow is documented and clear.
- The plugin is data-curation support — closer to a coding-workflow
  helper than a wet-bench research tool.
- The Required-Skill descriptions explicitly say "Not medical advice",
  which is the right disclosure shape for general-directory review.

After acceptance in general directory, reach out separately about
life-sciences cross-listing if the maintainer / Anthropic see it as
fitting. Do not block submission on it.

## Required artifacts (already in place)

| Required | Where it lives |
|---|---|
| Public GitHub repo URL | https://github.com/romeo111/task_torrent |
| Plugin source path inside repo | `plugins/openonco-contributor/` |
| `.claude-plugin/plugin.json` (validated) | [link](../plugins/openonco-contributor/.claude-plugin/plugin.json) |
| `.claude-plugin/marketplace.json` at repo root (validated) | [link](../.claude-plugin/marketplace.json) |
| README explaining the plugin | [README.md](../plugins/openonco-contributor/README.md) |
| ≥3 working examples | [EXAMPLES.md](../plugins/openonco-contributor/EXAMPLES.md) — 6 scenarios incl. refusals |
| Privacy policy | [PRIVACY.md](../plugins/openonco-contributor/PRIVACY.md) |
| Security / vulnerability reporting | [SECURITY.md](../plugins/openonco-contributor/SECURITY.md) |
| Support contact | [SUPPORT.md](../plugins/openonco-contributor/SUPPORT.md) |
| LICENSE | [LICENSE](../LICENSE) (MIT) at both repo root and plugin root |
| CHANGELOG | [CHANGELOG.md](../plugins/openonco-contributor/CHANGELOG.md) |
| CI for plugin manifest validation | `.github/workflows/plugin-validate.yml` |

## Steps (in submission order)

1. **Land the architecture-mismatch fix and end-to-end run**
   (handoff plan Steps 2 + 5). Submission should not happen with
   `claimable=0` on the landing page or with no observed contributor
   PR.

2. **Tag the release**:
   ```bash
   claude plugin tag plugins/openonco-contributor --push
   ```
   This produces `openonco-contributor--v0.4.0` and pushes the tag.
   Anthropic uses tag identity for plugin versioning when listed.

3. **Verify install from the public GitHub URL** (not local path):
   ```text
   /plugin marketplace add https://github.com/romeo111/task_torrent
   /plugin install openonco-contributor@tasktorrent
   ```
   Run on a machine without the local repo checkout. Confirm
   `/openonco-contribute` appears and the skills are discovered.

4. **Get OpenOnco maintainer endorsement** via a public artifact —
   issue, PR, or comment on `romeo111/OpenOnco` confirming the plugin
   is sanctioned. Anthropic likely wants this trail to confirm the
   plugin represents the consumer project officially.

5. **Submit via the form** — either:
   - https://claude.ai/settings/plugins/submit, or
   - https://platform.claude.com/plugins/submit

   Provide:
   - Repo URL: `https://github.com/romeo111/task_torrent`
   - Plugin path: `plugins/openonco-contributor/`
   - Plugin name: `openonco-contributor`
   - Version: `0.4.0`
   - Brief description: copy from `plugin.json` `description` field
   - Privacy / Security / Support URLs: link to the three docs above
   - Notes: link to handoff plan and submission strategy docs

6. **Wait for review**. Anthropic's SLA is not publicly documented.
   If/when feedback arrives, address in a follow-up PR. Do not change
   the plugin's safety contract without the OpenOnco maintainer's
   approval.

7. **(Optional) Life-sciences cross-listing**: after general-directory
   acceptance, open an issue at `anthropics/life-sciences` proposing
   addition. Frame as "oncology data-curation contributor plugin —
   non-MCP, non-clinical-decision-support, drafts only." Be willing to
   be told it's out of scope for that marketplace.

## What to avoid in the submission

- Do not pitch the plugin as a clinical-decision-support tool. It is
  not, and the description deliberately rules that out.
- Do not pitch it as bundled with the unshipped clinical-review plugin.
  That is a separate later track with stricter compliance work.
- Do not over-promise on PHI handling. v1 doesn't process PHI; the
  clinical-review track is where PHI screening becomes load-bearing.
- Do not promise auto-merge or auto-publish. Plugin produces drafts
  only.
- Do not omit the "Not medical advice" disclosure. It already lives in
  the description; keep it visible in submission copy.

## Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Anthropic rejects on "could be confused with medical-advice tool" | Medium | Description carries "Not medical advice"; refusals are smoke-tested; EXAMPLES has explicit refusal cases |
| Anthropic asks for more examples | Low | We have 6, including 2 refusals + 1 between-wave |
| Anthropic asks for a contributor demo / video | Medium | Step 5 of handoff plan addresses this — get a real PR through first |
| Life-sciences listing rejected | Low | Not blocking; submission still proceeds via general directory |
| Anthropic requires bundled MCP for science plugins | Low | Only an issue if life-sciences listing is the only goal; general directory does not require MCP |

## Done when

- Plugin tag `openonco-contributor--v0.4.0` exists on `main`.
- Public install via `https://github.com/romeo111/task_torrent` works
  on a fresh machine.
- One contributor PR has landed in `romeo111/OpenOnco` using the
  plugin.
- OpenOnco maintainer endorsement exists in a public issue/PR.
- Submission form filed with all artifacts linked.
- Anthropic listing accepted (or feedback returned and addressed).
