# OpenOnco Drop Pack: Pancreatic Biomarkers

## Pack ID

openonco-pancreatic-biomarkers-1drop

## Mission

Improve pancreatic cancer biomarker coverage through structured, source-linked, maintainer-reviewable outputs.

## Total

1 Drop

## Required Skills

- Biomarker extraction
- Citation verification

## Output Format

Submit structured biomarker entries, source links, notes on unsupported claims, and a short review report. Do not provide medical advice or treatment recommendations.

## Chunks

| Chunk ID | Chunk | Drop Estimate | Scope |
| --- | --- | ---: | --- |
| openonco-pancreatic-biomarkers-c1 | KRAS biomarkers | 0.2 Drop | Identify KRAS-related biomarker content candidates and source-linked evidence fields. |
| openonco-pancreatic-biomarkers-c2 | DNA repair biomarkers | 0.2 Drop | Identify DNA repair biomarker content candidates and source-linked evidence fields. |
| openonco-pancreatic-biomarkers-c3 | Immunotherapy biomarkers | 0.2 Drop | Identify immunotherapy-related biomarker content candidates and source-linked evidence fields. |
| openonco-pancreatic-biomarkers-c4 | Emerging biomarkers | 0.2 Drop | Identify emerging biomarker candidates only when source support is clear. |
| openonco-pancreatic-biomarkers-c5 | Normalization + citation review | 0.2 Drop | Normalize submitted fields and flag unsupported, unclear, duplicate, or broken citations. |

## Safety Checklist

- No medical advice
- No treatment recommendations
- No patient-specific outputs
- Source links required for every clinical claim
- Unsupported claims must be flagged
- Maintainer review required before publication

## Acceptance Criteria

- Output stays inside assigned chunk scope.
- Every clinical claim has a source link.
- Existing entries are updated by stable ID where possible.
- Duplicate candidates are flagged.
- Reviewer can trace each proposed change to source material.

## Rejection Criteria

- Recommendation wording is used.
- Sources are missing or fabricated.
- Output contains patient-specific guidance.
- PR changes unrelated files or unrelated disease areas.
