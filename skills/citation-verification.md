# Skill: Citation Verification

## Purpose

Check whether claims are supported by cited sources. This skill helps maintainers identify supported, unclear, unsupported, and broken-link citations.

## Input

- Project name
- Claim text or claim ID
- Citation URL or source reference
- Current page or dataset context
- Allowed source rules
- Existing citation format rules

## Output Schema

```yaml
citation_check:
  stable_id: string
  claim_id: string
  claim_text: string
  citation_url: string
  support_status: supported | unclear | unsupported | broken_link
  rationale: string
  suggested_action: keep | revise | remove | replace_source | maintainer_review
  contributor: string
  chunk_id: string
```

## Support Status

- supported: the cited source directly supports the claim.
- unclear: the source may be relevant, but support is partial, ambiguous, or difficult to confirm.
- unsupported: the source does not support the claim.
- broken_link: the citation cannot be reached or resolved.

## Rules

- Check the citation against the claim.
- Do not invent replacement citations.
- Do not treat related topic coverage as direct support.
- Do not rewrite clinical claims as fact unless maintainers requested the edit.
- Every suggested replacement source must be real, accessible, and clearly marked for review.
- Use maintainer_review when uncertain.

## Good Output

```yaml
citation_check:
  stable_id: "openonco-citation-verification-c3-row-001"
  claim_id: "claim-001"
  claim_text: "Claim text under review."
  citation_url: "https://example.org/maintainer-approved-source"
  support_status: "unclear"
  rationale: "The source appears related but direct support needs maintainer review."
  suggested_action: "maintainer_review"
  contributor: "github-user"
  chunk_id: "openonco-citation-verification-c3"
```

## Bad Output

```yaml
citation_check:
  stable_id: ""
  claim_id: "claim-001"
  claim_text: "Claim text under review."
  citation_url: "https://broken.example"
  support_status: "supported"
  rationale: "Probably true."
  suggested_action: "keep"
  contributor: "github-user"
  chunk_id: "openonco-citation-verification-c3"
```

The bad output marks support without checking and ignores the broken or unverified source.
