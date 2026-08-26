---
title: Conventions
type: reference
tags: [conventions]
status: accepted
version: 1.1.0
created: 2026-08-23
updated: 2026-08-25
---

# Conventions

Working conventions for Kai and AI agents, applied across all projects.
One subfolder per area. Each area has a `README.md` index; numbered files
give the reading order.

## Purpose - and non-purpose

This repo is a **documentation pool**: the reference for our conventions,
written for humans and agents to read and consult.

- **Verbose is fine when it serves a purpose.** Rationale, background,
  examples, alternatives considered, war stories - all belong here.
  Brevity is not a goal in itself; clarity and completeness of context
  are. An entry should answer *what*, *why*, and *when*, not just issue
  imperatives.
- **This repo is NOT an agent initiation skill.** The terse, imperative
  distillations that agents load at project start (`AGENTS.md`
  templates, skills, kickoff prompts) are separate artifacts. They are
  extracted FROM this pool, one-directionally, later. When writing here,
  do not pre-compress for an imagined loader - write the full picture;
  extraction picks what it needs.

Practical consequences:

1. Every convention entry records **why**, not only what.
2. Agent-facing summaries live in the consuming project (its
   `AGENTS.md`), pointing here for depth - never the reverse.
3. A bare rule list with no recorded why is a gap: either add the why or
   mark the entry as extraction-ready material.

## Areas

| Area | Scope |
|---|---|
| [`wiki/`](wiki/README.md) | Knowledge base / wiki work: frontmatter, Obsidian, versioning, human-agent collaboration, dynamic views |
| [`development/`](development/README.md) | Software development: git, lifecycle, project structure, standard files, languages, documentation, packaging/deployment |
| [`agents/`](agents/README.md) | Standard `AGENTS.md` template for repositories plus content rationale - copied into projects and specialized |

## Rule tiers

Every section in a conventions file is marked with its tier:

| Tier | Meaning | Deviating |
|---|---|---|
| **(rule)** | Binding everywhere. Safety, integrity, data-loss prevention, agent guardrails. Written as MUST/NEVER. | Only by explicit decision, recorded here in this repo. |
| **(default)** | Standard for **new** projects. Existing projects adopt when convenient. | Allowed - note the deviation in the project's `README.md`/`AGENTS.md`, that's it. |
| **(pattern)** | A proven solution from an existing project, documented for reuse. No obligation. | Free. Copy when useful. |

Unmarked prose is descriptive context, not a rule.

## How conventions work

1. **(rule) sections bind once this file is `status: accepted`.** Drafts
   are proposals.
2. **Projects opt in by reference.** A project's `AGENTS.md` points here;
   project-specific conventions live in the project and win over
   defaults from this repo.
3. **Changes are git commits.** Propose -> discuss -> commit. Agents may
   edit drafts; humans accept. Tier changes (default -> rule) need
   explicit human sign-off.
4. **Rules stay unambiguous and verifiable** - a convention nobody can
   follow or check is a wish. The prose around rules may be as verbose
   as useful (see [Purpose](#purpose--and-non-purpose)).

## File conventions for this repo

- Markdown, one topic per file, numbered prefixes for reading order.
- Every file starts with YAML frontmatter following the wiki schema
  ([`wiki/01-frontmatter.md`](wiki/01-frontmatter.md)): `title`, `type`,
  `tags`, `status`, `created`, `updated`.
- Entries carry rationale and examples; tier markers classify each
  section (see above).
- Grounded in real practice: defaults and patterns reflect what existing
  projects already do unless a rule explicitly changes that.
- **Standalone** *(rule)*: these documents name no concrete personal
  projects, apps, hosts, or accounts. Patterns describe shape; grounding
  examples live where the projects live.
- **Encoding** *(rule)*: all Markdown files are UTF-8 **without BOM**;
  prefer ASCII punctuation. Scripted/bulk edits MUST read and write
  explicit UTF-8 (never shell-default encodings) and are followed by a
  mojibake scan (`[\u00C0-\u00FF\u0152\u0153\u20AC\uFFFD]` must find
  nothing).
- **Versioning** *(rule)*: the repository version lives in the
  frontmatter above, follows SemVer (major = breaking *(rule)* changes
  or chapter removals ,  minor = new rules/defaults/chapters ,  patch =
  wording), is recorded in `CHANGELOG.md`, and every release is tagged
  `v<version>`. External documents that follow these conventions cite
  the version they were written against.

## License

Code: none (this repo contains no software). Documentation and
conventions text: **CC-BY-SA-4.0** - attribute
(the author), share adaptations under the same
license. See `LICENSE`.
