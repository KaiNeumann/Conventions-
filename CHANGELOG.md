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

## [2.0.0] - 2026-09-16

### Changed

- Clarify the wiki publication boundary: authorized personal information may
  live in restricted private knowledge vaults; public templates use placeholders.
  Secrets remain prohibited in ordinary notes, and derived outputs inherit access
  restrictions. This owner-approved clarification was recorded on 2026-09-07;
  no release or tag has been created.
- Make the wiki editor chapter editor-agnostic: rename
  `wiki/03-obsidian-setup.md` to `wiki/03-editor-setup.md` and remove the
  remaining "Obsidian is the concrete tool" framing from the wiki area,
  the area index, and the dynamic-views and markdown-flavor chapters. The
  conventions now describe the editor as a view over a plain Markdown
  folder and no longer name a single editor. (A chapter rename is a
  breaking change.)

### Added

- Harness-independent validation for indentation-sensitive files, with shared
  validation CLI adoption guidance for new and existing projects
- Wiki Markdown flavor: Obsidian-style image sizes (`![alt|400]`,
  `![alt|400x250]`) with Markview live-preview support and a Pandoc
  Lua filter for PDF output

## [1.9.0] - 2026-08-31

### Added

- Archify diagram chapter (pattern): interactive HTML alternative to
  Mermaid for shareable, explorable diagrams — when to reach for it,
  vendored skill location in `agent-skills`, authoring discipline, and a
  Mermaid-vs-Archify comparison table

## [1.8.0] - 2026-08-30

### Added

- Desktop packaging pattern: stable "latest" binary overwritten by the
  builder plus versioned historical copies
  (`App-<version>-<YYYYMMDD>-<HHMM>.exe`), keeping `dist\` intact while
  cleaning `build\`, the build venv, and `src\app\static\dist`
- Cross-platform defaults: portable (self-contained) desktop artifacts,
  and cross-compilation as the standard route for target-OS binaries

### Changed

- Windows cross-build strategy promoted from an open decision to an
  accepted default (Wine-based cross-builds on a Linux runner), now the
  single consistent story across the packaging, cross-platform, and
  task-automation chapters

## [1.7.0] - 2026-08-29

### Changed

- Advanced Mermaid syntax now requires a successful render in the active
  project viewer; vendored source and upstream support are insufficient

## [1.6.0] - 2026-08-29

### Added

- Fixed-column Mermaid placement-matrix convention that separates service
  ownership from request, proxy, data, and control-flow relationships

## [1.5.0] - 2026-08-29

### Added

- Diagram-set convention for complete architecture overviews: landscape,
  runtime placement, management and delivery, and request-path views

### Changed

- Architecture-diagram guidance now makes rendered peer equivalence, primary
  lanes, scope separation, and Mermaid `subgraph` limitations explicit

## [1.4.0] - 2026-08-29

### Added

- Architecture-diagram convention for Mermaid system-context and container
  overviews: scope, abstraction level, visual vocabulary, readable layouts,
  security/accessibility context, and diagram-as-code maintenance

## [1.3.0] - 2026-08-29

### Added

- Architecture and pipeline conventions covering provider boundaries,
  acquisition, extraction, normalization, validation, and AI integration
- GUI productivity patterns for tables, large collections, list-detail
  layouts, responsive disclosure, framework starting points, and
  browser-safe keyboard interaction
- Agent rationale chapter alongside the copyable `AGENTS.md` template

### Changed

- GUI classification now separates delivery mode from interaction profile;
  framework density informs sizing without overriding accessibility or task
  requirements
- Development lifecycle, automation, logging, and settings guidance now makes
  deterministic checks and operational boundaries explicit
- Agent capability boundaries and AgentSkills references clarified
- Dockerized-service lifecycle boundaries and project host-port reservation
  documented
- Wiki Markdown flavor aligned with Markview and linked to CommonMark and GFM
  references

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
