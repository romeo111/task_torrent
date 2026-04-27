# OpenOnco First Case

## Pilot Role

OpenOnco is the first pilot case for TaskTorrent. It is useful because it has structured knowledge needs, citation-sensitive content, and clear maintainer review requirements.

The TaskTorrent model must remain general. OpenOnco should test the pack and review workflow, not define the limits of the platform.

## Initial Pack Categories

- Biomarker evidence mapping
- Drug evidence mapping
- Citation verification
- Disease page improvement
- Dataset normalization

## Default Demand Queue

If a contributor has no topic preference, route them to the OpenOnco demand queue.

The initial demand queue should prioritize:

- Citation verification for existing content
- High-impact biomarker coverage gaps
- Normalization work that reduces reviewer burden
- Disease pages with clear maintainer-provided scope
- Dataset cleanup that has deterministic acceptance criteria

## Safety Boundary

OpenOnco work must not provide medical advice, treatment recommendations, or patient-specific outputs. Contributors should map evidence, verify citations, normalize data, and prepare reviewable drafts.

Every clinical claim must include source links. Every AI-generated output must be reviewed by maintainers before publication.

## Open Questions For OpenOnco Maintainers

- What source types are allowed for each evidence category?
- What citation format should contributors use?
- What data schema should biomarker outputs target first?
- Which diseases and biomarker groups have the highest priority?
- Who reviews each pack category?
- How should duplicate evidence entries be merged?
- What minimum evidence fields are required before a PR is reviewable?
- Should contributors edit existing files directly or submit structured sidecar files first?
