# Changelog

## v0.4.0 - First Public Release

TaskTorrent v0.4.0 is the first public release of the protocol.

### Added

- Chunk specification for reviewable AI-assisted contribution work.
- Cross-repo contract between TaskTorrent, consumer projects, and contributor
  agents.
- OpenOnco pilot chunk shelf and operating docs.
- Safety rules for citation-sensitive and high-stakes domains.
- Optional Python tooling:
  - `tasktorrent-lint` for chunk-spec validation.
  - `tasktorrent-init` for consumer-repo scaffolding.
- Zero-code onboarding prompt for maintainers who want to start by asking an
  agent to draft a TaskTorrent integration plan.

### Release Boundary

v0.4.0 is not a hosted service, marketplace, payment system, token economy, or
autonomous publishing workflow. It is a GitHub-native coordination protocol
designed around human maintainer review.

### First Pilot

OpenOnco is the first TaskTorrent pilot. The initial work covers biomarker
evidence reconstruction, citation verification, translation review, source-stub
ingestion, and dataset normalization under strict safety boundaries.
