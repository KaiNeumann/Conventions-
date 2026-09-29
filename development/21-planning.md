---
title: Planning and Scope Control
type: reference
tags: [conventions, development, planning, scope]
status: accepted
created: 2026-09-29
updated: 2026-09-29
---

# Planning and Scope Control

A plan file is the mechanism that keeps a piece of work inside its declared
boundary. This chapter covers what a plan must contain, which surface owns the
scope when two of them disagree, how a scope override has to be recorded, and
why a plan's own evidence table is the easiest place in a repository to write
an unverified claim that later agents believe.

Scope discipline for people is a matter of restraint. For an agent it is a
matter of artifacts: a boundary nobody wrote down cannot be violated, because
there is nothing to violate.

## When a plan is required *(rule)*

A plan file **MUST** exist before work begins when any of these hold:

1. the work spans more than one phase, component, or subsystem
2. the work can be executed in a session that will not finish it
3. the work carries a release, a migration, or a deletion
4. the work has a plausible boundary that someone could disagree with

A single-file fix does not need one. The test is not size, it is whether the
scope is contestable.

**Where it lives *(rule)*:** under `docs/`, never at the repository root
([documentation standards](06-documentation.md#deeper-docs-docs-default)). Name
it for what it plans (`docs/<area>/<subject>-plan.md`) and give it a status
line, so a reader can tell a live plan from a historical record in one glance.

**Status line *(rule)*:** `draft`, `active`, or `complete`, with the date of the
last substantive change. A plan that is executed but never flipped to
`complete` is indistinguishable from a plan that was abandoned halfway.

## Anatomy *(rule)*

A plan **MUST** carry these sections. The order is the reading order an agent
needs when it is about to make a decision, not an aesthetic preference.

### 1. Goal

One sentence naming the outcome. Not the activity. "Replace the desktop shell
so one window serves the whole product" is a goal; "migrate the UI" is a
restatement of the ticket.

### 2. Scope boundary

Two lists, both mandatory, both specific enough to be checked against a path:

```markdown
**In scope:**
- ...

**Out of scope for this plan, deliberately:**
- <path or component> - <why, and where it is scheduled instead>
```

The out-of-scope list is the section that does the work. Naming a path that
must not be touched converts a scope decision from a judgement call into a
lookup. "Do not touch the other application" is a preference; "the shared
legacy widget kit stays until the next release" is a boundary.

An empty out-of-scope list is a signal that the boundary has not been thought
about, not a sign of a clean project.

### 3. Work

Phases, in order, each with its own acceptance criteria. A phase is done when
its criteria are met, not when its code compiles and not when the agent stops
working on it.

### 4. Deliberate omissions

The things this plan chose not to do, with the reason. This is the
overengineering brake described in the
[interaction protocol](../agents/04-agent-communication-protocol.md#6-overengineering-rule):
each entry is a decision already made, so a later session does not reopen it.

### 5. Acceptance gates

A table. Every row names a command. See
[Evidence in the plan](#evidence-in-the-plan-rule) below.

## The plan is the only scope authority *(rule)*

An agent session typically carries two planning surfaces: the plan file on
disk, and a session-local work list. They are not equal, and the file wins.

**An item that is not in the plan is not work.** Before an item enters the
session-local list it is added to the plan, or it is dropped. The local list is
a view of the plan's current phase, never a second backlog.

Why this is a rule and not advice: the local list is what an agent actually
follows while it works. It is unbounded, it survives context compaction, and
nobody reviews it in a diff. A boundary that lives only in a file the agent read
once at the start loses to a list it re-reads on every step. This is the
mechanism behind most scope drift, and it is invisible from the plan file,
which still looks correct afterwards.

## Decision checkpoint *(rule)*

Immediately before an action that touches a path named in the plan's
out-of-scope list, the agent **MUST** state which line of the scope boundary it
is overriding, why, and record the override in the plan as a dated entry.

The override is permitted. Boundaries move; that is normal. What is not
acceptable is a boundary moving silently, because a silent move is
indistinguishable from never having had the boundary.

```markdown
## Scope overrides

- `<date>` - <path> moved into scope: <reason>. Deferred from <plan> to here.
```

The cost is a paragraph. The benefit is that a reviewer reading the diff sees
the scope change where it happened, and the next session inherits a plan that
matches the repository.

## Evidence in the plan *(rule)*

Every acceptance gate **MUST** name the command that proves it, and a gate
**MUST NOT** be marked met on the strength of a summary written by the party
that did the work.

| # | Gate | Command | Status | Recorded |
|---|---|---|---|---|
| 1 | <observable outcome> | `<command>` | `unmet` | |

Status vocabulary, deliberately small:

| Status | Meaning |
|---|---|
| `unmet` | Not yet satisfied, or not yet checked |
| `met` | The named command ran and its recorded output shows the gate holds |
| `partial` | The command ran and shows the gate holds for part of its claim |
| `withdrawn` | The gate is obsolete; say why in the plan |

Three rules make the table worth something:

1. **A gate names a command, not an intention.** "Verified against the
   packaged artifact" is not a command. `<package command> && <launch command>`
   is.
2. **The implementer does not self-certify in prose.** The person or agent
   that built the thing is the worst possible witness for whether it works,
   and the bias is invisible from inside. Where a mechanical check exists, the
   check fills the row.
3. **A gate that cannot be checked stays `unmet`.** An unmeasured gate is the
   honest state. "Met" for something nobody can re-run is a claim with a table
   around it.

Rationale, stated plainly: a plan's evidence table is the highest-trust text in
a repository. Every later session reads it as fact, because it is written in
the shape of a fact. A table filled in optimistically is worse than no table,
because it launders an unverified claim into something a reviewer will not
re-check.

## One plan, one session *(default)*

A session should execute one plan. A session that must cross into a different
release, a different application, or a different problem class **SHOULD** end
with a handoff rather than continue.

Long sessions are the multiplier behind every other failure in this chapter.
Scope erosion, invented blockers, and unverified completion claims all become
more likely as a session accumulates unrelated workstreams, because the
early context is gone and only the work list survives. Splitting the session
is cheaper than auditing it.

A handoff records: what is done, what is in flight, what the next session must
read first, and the exact state of the working tree. Most harnesses can write
one automatically at a context rollover or on demand; where that exists, use
it rather than composing one by hand.

## Plan lifecycle *(default)*

1. **Draft** - written before implementation, status `draft`.
2. **Active** - work started, status flipped, `updated` bumped.
3. **Per phase** - the phase is marked done when its acceptance criteria are
   met, not when the agent moves on.
4. **Complete** - every gate is `met`, `partial`, or `withdrawn`, and any
   `partial` or `withdrawn` row says what remains.

Plans are historical records once complete. Keep them; do not rewrite them to
match what happened. A plan that has been edited to agree with reality cannot
answer the only question a reader has, which is what was decided at the time
and why.

## Anti-patterns

- A plan with a goal and a task list but no out-of-scope section. This is the
  most common shape and it does not constrain anything.
- Acceptance gates written as prose claims instead of commands.
- A gate table updated in the same session that implemented the work, with no
  command output behind it.
- A session-local work list used as the backlog, with the plan file updated at
  the end to match.
- One plan covering two releases, on the theory that the work is related.
- A plan edited after completion so it reads as though the original scope was
  always this.
- Reopening a deliberate omission because it looks like an improvement. That
  is a new plan, or a dated scope override.

## Review criteria

A plan is in good shape when a reader who has not seen the work can answer:

1. What is the outcome, in one sentence?
2. What is explicitly not being done, and where is that scheduled instead?
3. What command proves each acceptance gate?
4. Did any gate move to `met` without a recorded command?
5. Is there a dated scope override, and is it dated?

If question 4 has an uncomfortable answer, the table is decoration and should
say `unmet` until it is not.

## Rationale

A plan file is cheap to write and cheap to review. The failure it prevents is
expensive in a specific way: scope drift stays invisible until the diff is
read, at which point the wrong work is finished rather than merely started.
The rules above are the minimum that makes the file binding: a named
out-of-scope list, one authority for scope, a recorded override path, and an
evidence table that a command can fill.
