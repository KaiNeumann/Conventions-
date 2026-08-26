---
title: Creating an AGENTS.md
type: reference
tags: [conventions, agents]
status: accepted
created: 2026-08-25
updated: 2026-08-25
---

# Creating an AGENTS.md

Every repo an agent regularly works in **MUST** have an `AGENTS.md`
(required by [`../development/06-documentation.md`](../development/06-documentation.md)
and the standard-files chapter). It is written for agents but read
top-down like any document - its structure decides whether constraints
actually hold.

## Workflow

1. Copy [`AGENTS.md.template`](AGENTS.md.template) to the repo root as
   `AGENTS.md`.
2. Fill every `<placeholder>`; delete sections that genuinely do not
   apply.
3. Record the conventions baseline version (see the standard-files
   chapter, [`../development/04-repo-standard-files.md`](../development/04-repo-standard-files.md)).
4. Specialize the Known gotchas with wrong/right pairs as they are
   learned.
5. Keep it under ~200 lines - depth belongs in `docs/`, hot rules up
   front.
6. Improvements to the generic parts feed back into this repository
   first (rule of origin).

## Required sections and why

### Safety gates first *(rule)*

Agents read instructions top-down and act immediately. Anything that
must constrain behavior has to appear before any task description -
secret handling, destructive commands, project-specific red lines. A
gate at the bottom is a gate that was already violated.

### Automation contract

The largest recurring cost in agent-driven development is hand-running
verification that CI performs anyway. Stating the contract (push
triggers CI - no local pre-runs except debugging - fix from log tails)
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

## Naming and loading safety *(rule)*

The copyable template ships as **`AGENTS.md.template`**: the `.template`
extension keeps harnesses from auto-loading the conventions repo itself,
while a project's real file is always plain `AGENTS.md`. Never commit an
unrenamed copy.
