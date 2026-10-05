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

## [2.4.0] - 2026-10-05

### Added

- `development/02-lifecycle.md`: new `User data protection` *(rule)*
  section. User data (database entries, files, runtime state) MUST be
  backed up with a known restore path before any delete, move, or
  manipulation; archives and other input data are immutable; metadata
  MUST NOT be deleted on the unverified assumption that the original
  data is gone (check mount, path, permissions first); work on
  productive apps MUST start by verifying the actual system, database,
  volume, and identity in effect.
- `development/02-lifecycle.md`: `User data protection` *(rule)*
  extended. Productive user data MUST live in databases, volumes, and
  identities separate from test and development data, unreachable by
  default from test runs; tests use synthetic or copied data, never
  the productive store. The Why carries an anonymized war story: a
  redeploy with an unreadable library mount let a startup scan prune
  3,951 rows of irreplaceable metadata with no backup on the server.

## [2.3.1] - 2026-10-03

### Changed

- `agents/04-agent-communication-protocol.md`: clarify the existing
  communication rule to prefer neutral, literal status reporting over
  management jargon, colloquialisms, and performative assurances.

## [2.3.0] - 2026-09-29

### Added

- Planning chapter in the development area, `development/21-planning.md`,
  covering plan files as a scope boundary. Sections: when a plan file is
  required and where it lives; plan anatomy (goal, scope boundary with a
  mandatory out-of-scope list, phases with acceptance criteria, deliberate
  omissions, acceptance gates); the rule that the plan file is the only
  scope authority and a session-local work list is a view of it; the decision
  checkpoint requiring a dated, cited scope override; evidence rules for the
  gate table, including a status vocabulary and the rule that a gate names a
  command and is not marked met on the implementer's own summary; one plan
  per session with a handoff at the boundary; plan lifecycle; anti-patterns;
  and review criteria. Filed as `status: accepted`, so the *(rule)* sections
  bind.

### Changed

- `development/02-lifecycle.md`: the plan stage now points at the planning
  chapter and asks for an out-of-scope list and command-named gates instead
  of a bullet list inside an issue.
- `development/02-lifecycle.md`: iteration discipline item 4 reversed. It
  previously advised keeping a session log only when work spanned sessions
  and treating git history as the log otherwise, which is the wrong default
  for agent work: git history records what changed, not what was decided or
  still open. It now advises one plan per session and handing off at a
  boundary.
- `development/README.md`: chapter 21 added to the reading order.
- `README.md`: development area scope now names planning and scope control.

## [2.2.1] - 2026-09-28

### Fixed

- Four broken references found by a repo-wide link and anchor check:
  the `Purpose` self-link in the root `README.md` pointed at
  `#purpose--and-non-purpose` instead of `#purpose---and-non-purpose`;
  the standard-files chapter linked `15-settings.md`, which does not
  exist (settings is `14-settings.md`); the development index linked
  `` `16-work-tracking.md` `` with the backticks inside the link target,
  which breaks the link; and the frontmatter chapter anchored to
  `#indentation-sensitive-validation` instead of the actual heading
  `#indentation-sensitive-validation-rule`.

## [2.2.0] - 2026-09-28

### Added

- Agent interaction protocol chapter in the agents area, adopted from a
  standalone protocol document: task-start acknowledgement, goal
  retention, clarification before assumption, scope-creep stop, smallest
  sufficient change, communication density, failure handling,
  user-interruption priority, completion reporting, the default decision
  order, and the `AGENTS.md` integration pattern. Each section carries a
  tier marker and its rationale; sections 1-10 and 13 are *(rule)*,
  sections 11-12 are *(default)*. The chapter and its tier assignment
  were owner-approved on 2026-09-28, so the file ships as
  `status: accepted`. Review points are tracked in `TODO.md`: about one
  month after adoption, then again after three.

## [2.1.0] - 2026-09-28

### Added

- Windows browser automation chapter: the account-lockout hazard for
  automated browser work, attribution discipline for the Security log
  (elevation, distinguishing "unreadable" from "no events", elevated
  collector artifacts, unconditional account-name redaction), shared
  Chromium hardening across every launch site including live-test
  harnesses, proxy-credential stripping at the sink, machine-level
  containment, a debugging playbook, and a war story covering a hardening
  fix that was correct but was not the cause. The chapter's two *(rule)*
  sections were owner-approved on 2026-09-28, so the file ships as
  `status: accepted`.

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
