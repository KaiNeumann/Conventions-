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

## [1.2.0] - 2026-08-25

### Added

- Operations area with dockerized-services standards: standalone compose
  stacks, edge routing with default SSO, non-root and socket
  restrictions, segmented networking, stdout-first container logging,
  lifecycle rules; third-party image hardening subsection
  (no-new-privileges, cap-drop-all with explicit adds, host network as
  documented exception)
- Work tracking chapter: TODO.md queue structure, entry anatomy with
  priority/kind/area headline tags, cold-start body requirements,
  promotion rules to remote issues
- Agents chapters: MCP servers (accepted / candidates / rejected
  taxonomy, admission criteria, codebase-memory-mcp evaluation) and
  agent skills (format rules, inventory snapshot including playwright,
  promotion path, third-party adoption review, decision block
  skill vs AGENTS.md vs command)

### Changed

- Encoding rule refined: UTF-8 without BOM plus no invisible
  characters, replacing the pure-ASCII-only wording
- MCP vocabulary unified ("accepted" instead of "sanctioned")

### Fixed

- Development index deduplicated after chapter renumbering; comma
  spacing artifacts from the character normalization sweep removed

## [1.1.0] - 2026-08-25

### Added

- GUI design chapter: app-class decision table (desktop-first vs
  web-first, per deployment), ten principles (keyboard-first, touch and
  pointer first, density by app type, designed states, first-run,
  automatability, vendored assets, local-first and installable, state
  persistence, undo over confirmation), visual tokens with status
  colors and optional theming, interaction standards (help overlay
  rule, search everywhere, drag & drop, tooltip timing with warm-window
  skip, declarative implementations), Lucide icons plus app identity
  mark, accessibility baseline
- Logging chapter: `logs/<app>.log` discipline, ISO timestamps with
  filterable identifiers (shape free per app), noise control
- Settings chapter: portable sidecar vs profile location, resilient
  loading, portability-aware sensitive-value protection, one settings
  truth
- Agents area: `AGENTS.template.md` plus section-by-section rationale
- Prose style rules (anti-AI-tell writing) and repo-wide pure-ASCII
  normalization outside code fences
- Outsider-first README standard with feature highlights

### Changed

- Development chapters renumbered into lifecycle clusters
  (Foundations / Craft / Design / Delivery / Operate & govern);
  `10-ci` refocused and renamed to `11-releases`
- Standalone policy enforced: portfolio names removed from all
  convention texts

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
