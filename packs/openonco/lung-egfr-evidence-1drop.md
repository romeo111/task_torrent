# OpenOnco Drop Pack: Lung EGFR Evidence

## Pack ID

openonco-lung-egfr-evidence-1drop

## Mission

Map EGFR-related lung cancer evidence into structured, source-linked, maintainer-reviewable outputs.

## Total

1 Drop

## Required Skills

- Drug evidence mapping
- Biomarker extraction
- Citation verification

## Output Format

Submit structured evidence mappings, source links, normalization notes, and citation verification status. Evidence mapping must not include "best treatment" claims or recommendation wording.

## Chunks

| Chunk ID | Chunk | Drop Estimate | Scope |
| --- | --- | ---: | --- |
| openonco-lung-egfr-evidence-c1 | EGFR mutation overview | 0.2 Drop | Prepare source-linked overview fields for EGFR mutation categories without recommendation language. |
| openonco-lung-egfr-evidence-c2 | Drug evidence mapping | 0.25 Drop | Map drug-related evidence fields with source links and neutral evidence wording only. |
| openonco-lung-egfr-evidence-c3 | Resistance mechanisms | 0.2 Drop | Map source-linked resistance mechanism fields without patient-specific interpretation. |
| openonco-lung-egfr-evidence-c4 | Citation verification | 0.2 Drop | Verify cited support and label each claim as supported, unclear, unsupported, or broken_link. |
| openonco-lung-egfr-evidence-c5 | Normalization pass | 0.15 Drop | Normalize names, IDs, citation format, and duplicate entries for review. |

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Source links required for every clinical claim
- Evidence wording must remain neutral
- Maintainer review required before publication

## Acceptance Criteria

- Output uses stable IDs where available.
- Drug evidence is mapped without recommendation wording.
- Each evidence entry includes source links.
- Citation verification status is explicit.
- Reviewer notes identify any unclear or unsupported material.

## Rejection Criteria

- Output ranks treatment options.
- Output says or implies what a patient should receive.
- Sources do not support mapped claims.
- PR includes broad unrelated rewriting.
