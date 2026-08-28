---
title: Agent Skills
type: reference
tags: [conventions, agents, skills]
status: accepted
created: 2026-08-25
updated: 2026-08-28
---

# Agent Skills

Skills are folders with a `SKILL.md` (YAML frontmatter: `name`,
`description`) that a harness loads on demand, optionally plus
`scripts/` and `references/`. House philosophy: **scripts and reference
files instead of prose** - the agent runs a command or reads a file
instead of re-deriving instructions every session. Accurate and cheap.

## Format *(rule)*

1. One folder per skill, named exactly like the `name` field
   (lowercase alphanumeric with single hyphens).
2. `description` is required and doubles as the trigger surface:
   front-load the keywords a user would actually say.
3. Heavy logic goes into `scripts/`, deep background into
   `references/` - the SKILL.md itself stays lean.
4. License field set (MIT by default); unknown frontmatter fields are
   ignored by loaders but kept minimal anyway.
5. Skills and prompts orchestrate capabilities; they do not contain
   business rules, parsers, or provider-specific application logic. Put that
   logic behind a tested library, CLI, API, or MCP tool that the skill calls.

## Inventory *(snapshot - the [shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills) is the source of truth for own skills)*

| Skill(s) | Origin | Purpose | Location |
|---|---|---|---|
| `ponytail`, `-audit`, `-review`, `-debt`, `-help` | own | Lazy-senior style enforcement: scope cuts, over-engineering audits, debt ledger | harness global skills dir |
| `env-probe` | own, [shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills) | One-call OS/shell/encoding/tooling snapshot so agents stop guessing | [shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills) |
| `model-config` | own, same repository | Project-scoped harness/model routing setup and audit | [shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills) |
| `security-research`, `security-review` | adopted third-party | Security assessment workflows | harness cache (installed copies) |
| `playwright` | built-in harness skill | Browser automation: navigation, screenshots, form interaction, visual verification of web UIs; pairs with project-scoped playwright MCP setups | built into the harness |

Locations: the **[shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills)** is the source of truth for
own skills; the harness global directory holds what every session needs;
project-local skill folders are experiments on their way up.

## Promotion path *(default)*

experiment (project-local) → proven ([shared skills repository](https://git.kaiuweneumann.de/kai/AgentSkills)) →
everywhere (harness global). Demotion happens when a skill stops
earning its trigger surface.

## Adopting third-party skills *(rule)*

1. Read the full `SKILL.md` before installing - skills are prompt
   content and therefore an injection surface.
2. Prefer permissive licenses (MIT) and no external calls inside
   scripts.
3. Installed copies live in the managed cache; re-review on major
   updates.

## Skill, AGENTS.md, or command? *(default)*

The same behavior can ship three ways - pick by *when* it should fire:

| Fires when | Ship as |
|---|---|
| Always, on every relevant action | a rule line in `AGENTS.md` |
| On demand, triggered by described intent | a skill |
| Only when explicitly invoked by name | a command |

A skill that ends up being invoked explicitly every time is really a
command; a rule needed only inside one workflow belongs in that
workflow's skill body.

## Writing quality *(default)*

1. One skill, one job. Two triggers mean two skills or a parameter.
2. Write the description last, after the body shows what it does.
3. If the body keeps growing, move steps into scripts - the file should
   read like a checklist, not a tutorial.
