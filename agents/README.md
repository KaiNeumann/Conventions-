---
title: Agents
type: reference
tags: [conventions, agents]
status: accepted
created: 2026-08-25
updated: 2026-08-25
---

# Agents

Standard agent instructions for repositories: a house `AGENTS.md`
template plus the reasoning behind every section.

| File | Purpose |
|---|---|
| [`AGENTS.template.md`](AGENTS.template.md) | Copy into a project root as `AGENTS.md`, fill the `<placeholders>`, specialize |
| [`02-mcp-servers.md`](02-mcp-servers.md) | Accepted MCP servers, admission criteria, removal policy |
| [`03-agent-skills.md`](03-agent-skills.md) | Skill format, inventory (own + adopted), promotion path |
| `README.md` (this file) | Content walkthrough and rationale |

## Lifecycle

1. **Copy, don't reference-only.** Agent harnesses load `AGENTS.md`
   from the repo they work in; a link elsewhere is invisible to them.
2. **Specialize**: fill placeholders (project name, safety gates,
   commands, settings locations), add gotchas as they are learned.
3. **Feed back**: improvements to the *generic* parts of the template
   belong in this repository first, then propagate out
   ([rule of origin](../development/README.md)).

> Naming note: the template lives as `AGENTS.template.md` so that
> harnesses auto-loading any `AGENTS.md` in a directory tree do not
> mistake the conventions repo for a project.

## Section-by-section rationale

### Safety gates first *(rule)*

Agents read instructions top-down and act immediately. Anything that
must constrain behavior has to appear before any task description -
secret handling, destructive commands, project-specific red lines. A
gate at the bottom is a gate that was already violated.

### Automation contract

The largest recurring cost in agent-driven development is hand-running
verification that CI performs anyway. Stating the contract (push triggers CI - no local pre-runs except debugging - fix from log tails)
converts that cost into a rule. See
[`../development/12-task-automation.md`](../development/12-task-automation.md).

### Global rules

Environment assumptions (OS/shell), portability (`pathlib`, no hardcoded
paths), encoding discipline, `temp/` usage, venv usage, and the testing
policy remove whole classes of guesswork - every one of these was once a
recurring failure mode.

### Architecture pointers

Agents break things fastest where structure is implicit. Naming the
canonical modules/entry points and explicitly listing frozen/deprecated
zones prevents building on dead code.

### Known gotchas

Traps that were expensive once (quoting rules, encoding, ordering
constraints) will be expensive again for the next agent - recorded as
wrong/right pairs, not prose.

### Privacy

Personal data must not leak through commits, issue texts, logs, or
example files; placeholders keep shared artifacts clean by construction.

### Prohibited without instruction

Scope discipline for agents: no drive-by edits, no sweeping unrelated
worktree changes into commits, no dependency additions without a stated
reason.
