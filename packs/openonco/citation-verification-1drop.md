# OpenOnco Drop Pack: Citation Verification

## Pack ID

openonco-citation-verification-1drop

## Mission

Verify and clean OpenOnco citations so maintainers can identify broken links, unsupported claims, unclear support, and formatting issues.

## Total

1 Drop

## Required Skills

- Citation verification

## Output Format

Submit a citation verification report with claim IDs or stable references, citation links, support_status, notes, and recommended maintainer action. Do not rewrite clinical content as fact unless the source support is clear and maintainers requested that edit.

## Chunks

| Chunk ID | Chunk | Drop Estimate | Scope |
| --- | --- | ---: | --- |
| openonco-citation-verification-c1 | Broken links | 0.15 Drop | Identify citations that fail to resolve or cannot be accessed. |
| openonco-citation-verification-c2 | Source relevance | 0.25 Drop | Check whether cited sources are relevant to the attached claims. |
| openonco-citation-verification-c3 | Unsupported claims | 0.25 Drop | Flag claims that are not supported by the cited source. |
| openonco-citation-verification-c4 | Citation format normalization | 0.15 Drop | Normalize citation format without changing claim meaning. |
| openonco-citation-verification-c5 | Final review report | 0.2 Drop | Summarize findings, duplicates, unresolved questions, and recommended maintainer follow-up. |

## Support Status Values

- supported
- unclear
- unsupported
- broken_link

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Do not invent replacement citations
- Mark uncertainty explicitly
- Maintainer review required before publication

## Acceptance Criteria

- Every checked claim has a support_status.
- Broken links are separated from unsupported claims.
- Notes explain why support is unclear or unsupported.
- Citation format changes are isolated from content changes.

## Rejection Criteria

- Fake replacement sources are added.
- Unsupported claims are rewritten as supported.
- Output changes clinical meaning without maintainer instruction.
- PR combines citation verification with unrelated edits.
