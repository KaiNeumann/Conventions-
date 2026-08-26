# Changelog

All notable changes to the conventions are recorded here. The version
applies to the repository as a whole (see `README.md` frontmatter);
releases are tagged `v<version>`.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/):

- **MAJOR** - breaking changes to *(rule)* sections, removed or renamed
  chapters/files
- **MINOR** - new chapters, new *(rule)*/*(default)* sections,
  non-binding additions
- **PATCH** - clarifications, wording, formatting

## [1.0.0] - 2026-08-25

Initial complete structure.

### Added

- Rule-tier system (rule / default / pattern) and standalone/no-names
  policy (root README)
- Development area: git, lifecycle, project structure, repo standard
  files, languages, documentation (outsider-first README standard),
  gui design (app classes, visual tokens, tooltip timing), packaging
  web/desktop, cross-platform, releases, task automation, logging,
  settings, licensing
- Agents area: `AGENTS.template.md` with rationale
- Wiki area: frontmatter schema (optional `realm`), page bundles,
  markdown flavor, obsidian setup, versioning/deprecation,
  human-agent collaboration tiers, dynamic views
