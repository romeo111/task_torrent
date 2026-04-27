# Skill: Biomarker Extraction

## Purpose

Extract structured biomarker information from maintainer-approved sources into a reviewable format. This skill supports evidence mapping and content improvement, not medical advice.

## Input

- Project name
- Disease or topic scope
- Biomarker scope
- Allowed sources
- Existing schema or target fields
- Existing IDs, if available

## Output Schema

```yaml
biomarker_entry:
  stable_id: string
  disease: string
  biomarker_name: string
  biomarker_category: string
  claim_summary: string
  source_links:
    - string
  support_status: supported | unclear | unsupported | broken_link
  notes: string
  contributor: string
  chunk_id: string
```

## Rules

- Stay inside the assigned disease, biomarker, and chunk scope.
- Do not provide patient-specific interpretation.
- Do not write treatment recommendations.
- Every clinical claim must include source links.
- Use neutral evidence wording.
- Mark uncertainty explicitly.
- Preserve stable IDs where available.
- Flag duplicates instead of adding near-identical entries.

## Good Output

```yaml
biomarker_entry:
  stable_id: "openonco-pancreatic-biomarkers-c1-row-001"
  disease: "pancreatic cancer"
  biomarker_name: "KRAS"
  biomarker_category: "gene"
  claim_summary: "Source-linked draft claim for maintainer review."
  source_links:
    - "https://example.org/maintainer-approved-source"
  support_status: "unclear"
  notes: "Needs maintainer review before publication."
  contributor: "github-user"
  chunk_id: "openonco-pancreatic-biomarkers-c1"
```

## Bad Output

```yaml
biomarker_entry:
  stable_id: ""
  disease: "any cancer"
  biomarker_name: "KRAS"
  biomarker_category: "important"
  claim_summary: "Patients with this biomarker should choose a specific treatment."
  source_links: []
  support_status: "supported"
  notes: "No source needed."
  contributor: "github-user"
  chunk_id: "unknown"
```

The bad output gives treatment guidance, lacks source links, exceeds scope, and marks support without evidence.
