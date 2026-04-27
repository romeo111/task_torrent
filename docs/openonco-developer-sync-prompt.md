# OpenOnco Developer Sync Prompt

> **Historical artifact (2026-04-27).** This was the original sync prompt drafted before the chunks-only model was adopted. It still references "Drop Packs"; the current model uses standalone Chunks (see `docs/chunk-system.md` and `docs/openonco-pilot-workflow.md`). The questions below remain useful as a maintainer-alignment checklist; the workflow answers in `docs/openonco-first-case.md` supersede the original prompt's assumptions.

Use this prompt to align OpenOnco maintainers and developers on the TaskTorrent pilot before creating execution issues.

```text
We are preparing TaskTorrent as a planning and coordination layer for distributed AI-assisted open-source work.

TaskTorrent is a torrent-like model for structured AI effort:
- Projects publish standardized work packages called Drop Packs.
- 1 Drop means about 100k tokens of structured AI work.
- Each Drop Pack is split into smaller Chunks, usually 0.15 to 0.3 Drop.
- Contributors use their own AI tools, such as Claude Code, Codex, Cursor, or ChatGPT, to execute chunks.
- Outputs are submitted through GitHub pull requests or structured files.
- Maintainers review everything before publication or merge.

Drop is only an effort estimate. It is not money, crypto, a transferable token, or a reward asset.

We would like OpenOnco to be the first pilot case because it has clear needs around structured evidence work, citation verification, biomarker mapping, data normalization, and disease page improvement. TaskTorrent should remain a general platform, but OpenOnco can help validate the first workflow.

Important safety boundaries for OpenOnco:
- No medical advice.
- No treatment recommendations.
- No patient-specific outputs.
- No fake citations.
- Every clinical claim must require source links.
- Every AI-generated output must be reviewed by OpenOnco maintainers before publication.

Proposed first Drop Pack categories:
- Biomarker evidence mapping
- Drug evidence mapping
- Citation verification
- Disease page improvement
- Dataset normalization

We need OpenOnco maintainer input on the following questions:
1. Which OpenOnco data schema should the first packs target?
2. Should contributors edit existing files directly, or submit structured sidecar files first?
3. What source types are allowed for biomarker and drug evidence mapping?
4. What citation format should contributors use?
5. Which disease areas, biomarkers, or citation cleanup tasks are highest priority?
6. Who should review each pack category?
7. What minimum fields make a submitted chunk reviewable?
8. How should duplicate or overlapping evidence entries be handled?
9. Are there existing labels, branch rules, or PR conventions we should follow?
10. What would make this workflow useful to OpenOnco maintainers without increasing review burden too much?

The immediate goal is not to build a production app. The immediate goal is to agree on a manual GitHub-based pilot:
- 3 to 5 initial Drop Packs
- 4 to 6 chunks per pack
- clear skill specs
- GitHub issue templates
- PR review checklist
- maintainer-owned acceptance criteria

Please review the TaskTorrent planning docs and tell us what should change before we open the first OpenOnco pilot issues.
```
