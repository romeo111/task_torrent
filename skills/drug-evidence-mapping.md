# Skill: Drug Evidence Mapping

## Purpose

Map drug-related evidence into structured fields for maintainer review. This is evidence mapping only.

## Input

- Project name
- Disease or topic scope
- Drug or drug class scope
- Biomarker or alteration scope, if relevant
- Allowed sources
- Target schema
- Existing IDs, if available

## Output Schema

```yaml
drug_evidence_entry:
  stable_id: string
  disease: string
  drug_name: string
  biomarker_or_context: string
  evidence_summary: string
  source_links:
    - string
  support_status: supported | unclear | unsupported | broken_link
  evidence_type: string
  notes: string
  contributor: string
  chunk_id: string
```

## Rules

- Evidence mapping only.
- Do not make "best treatment" claims.
- Do not use recommendation wording.
- Do not state what a patient should receive.
- Do not rank treatments.
- Every clinical claim must include source links.
- Use neutral wording such as "source describes", "source reports", or "evidence entry for review."
- Mark unclear, unsupported, or broken sources explicitly.
- Preserve stable IDs where available.

## Good Output

```yaml
drug_evidence_entry:
  stable_id: "openonco-lung-egfr-evidence-c2-row-001"
  disease: "lung cancer"
  drug_name: "example drug name from approved source"
  biomarker_or_context: "EGFR-related context"
  evidence_summary: "Neutral source-linked evidence summary for maintainer review."
  source_links:
    - "https://example.org/maintainer-approved-source"
  support_status: "unclear"
  evidence_type: "to_be_confirmed_by_maintainer"
  notes: "No recommendation wording included."
  contributor: "github-user"
  chunk_id: "openonco-lung-egfr-evidence-c2"
```

## Bad Output

```yaml
drug_evidence_entry:
  stable_id: ""
  disease: "lung cancer"
  drug_name: "example drug"
  biomarker_or_context: "EGFR"
  evidence_summary: "This is the best treatment and should be used."
  source_links: []
  support_status: "supported"
  evidence_type: "recommendation"
  notes: "Generated from memory."
  contributor: "github-user"
  chunk_id: "openonco-lung-egfr-evidence-c2"
```

The bad output makes a recommendation, lacks sources, and claims support without verification.
