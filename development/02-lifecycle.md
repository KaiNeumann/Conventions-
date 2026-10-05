---
title: Development Lifecycle
type: reference
tags: [conventions, development, process]
created: 2026-08-23
updated: 2026-10-05
---

# Development Lifecycle

## Stages (default)

```
idea → plan → implement → verify → document → commit → deploy
```

1. **Idea** - capture it (issue or `TODO-backlog.md`), one line is enough.
   Don't build it yet.
2. **Plan** - for anything beyond a trivial fix: a plan file with an
   explicit out-of-scope list, phases with acceptance criteria, and gates
   that name the command proving them. See
   [`21-planning.md`](21-planning.md). A bullet list inside an issue is
   enough only for work that fits in one sitting.
3. **Implement** - smallest change that satisfies the plan. Follow
   project-structure and language conventions. Tests alongside code, not
   "later".
4. **Verify** - quick local sanity on touched files (compile/lint);
   authoritative verification is the CI result on push
   ([`12-task-automation.md`](12-task-automation.md)). Local full-suite
   runs happen only in repos without CI or while debugging a red
   pipeline. Agents report evidence (command/CI output), not claims.
5. **Document** - README/AGENTS.md/docs updated in the same change if
   behavior, structure, or safety rules changed
   ([documentation conventions](06-documentation.md)).
6. **Commit** - per [git conventions](01-git.md); small atomic commits with evidence
   reviewed (`git status --short --ignored`).
7. **Deploy** - docker compose rebuild / packager run per packaging
   conventions ([web](08-packaging-web.md), [desktop](09-packaging-desktop.md));
   verify healthz after deploy.

## User data protection (rule)

User data - database entries, files, and runtime state created by or on
behalf of users - MUST be treated as irreplaceable, even when it looks
redundant or orphaned.

1. **Backup before delete, move, or manipulation.** Before user data is
   deleted, moved, or otherwise manipulated (migration, format
   conversion, ownership/permission change, bulk update - anything not
   undone by reverting one commit), a restorable backup MUST exist and
   the restore path MUST be known to work.
2. **Input and archive data is immutable.** Archives and other input
   data MUST NOT be changed, least of all deleted. Derive new data from
   them; never rewrite them in place.
3. **Missing data is a hypothesis, not a fact.** Metadata MUST NOT be
   deleted on the assumption that the original data is gone. An absent
   file or an empty query result can also mean a volume is not mounted,
   is mounted at the wrong path or read-only, or permissions hide the
   data. Verify mount, path, and permissions before concluding data is
   gone.
4. **Check assumptions against the productive system.** Work on
   productive apps and user data MUST start by verifying which system,
   database, volume, and identity are actually in effect - not the ones
   assumed. A destructive command against the wrong target is the
   failure this rule exists to prevent, not a mistake a backup excuses.
5. **Keep production data apart from test and development data.**
   Productive user data MUST live in separate databases, volumes, and
   identities from test and development data - never shared, never
   reachable by default from a test run. Tests and experiments MUST run
   against synthetic or copied data, never against the productive
   store. Production code MUST NOT write test fixtures into productive
   tables, and a test run MUST NOT be able to open a productive
   connection: distinct database names, credentials, and connection
   strings make the wrong-target error visible before it turns
   destructive.

Why: user data cannot be regenerated from source code. Every item above
is a past data-loss shape: a delete without a tested backup, an
"obsolete" archive that was the only original, metadata cleaned up
because the mount was empty, a correct command run against the wrong
environment, test data mixed into production until a cleanup or a test
fixture wiped real rows.

War story (anonymized): a media-manager service was redeployed while
its library mount was present but unreadable - wrong UID/GID for the
container user, so the app saw 8 files out of thousands. Its startup
scan treated "file not seen" as "file deleted" and pruned 3,951
database rows, taking years of manual tags and notes with it. No
backup existed on the server. A later permission fix then re-indexed
everything as blank rows, closing the forensic window. The lessons are
items 3 and 4 above: verify a mount is readable before any destructive
reconciliation runs, and never let a routine scan decide on its own
that missing means deleted.

## Definition of done (rule)

A task is done when ALL are true:

- [ ] Code works as specified (verified by running it, not assumed)
- [ ] Tests exist for new logic; suite green via CI (locally only when
      the repo has no pipeline)
- [ ] Lint/type checks clean on touched files
- [ ] Docs updated where they became wrong
- [ ] No secrets/local artifacts staged
- [ ] No process left running that this work started (see below)
- [ ] Committed per [git conventions](01-git.md)

(Small scripts and one-off tools may deliberately skip tests/docs -
say so, don't silently skip.)


## Process hygiene (rule)

**Never leave a process running after a test, a smoke, or a measurement.**

Anything started to *check* something - a dev server, a worker pool, a
benchmark, a profiling run - is torn down when the check is over, including
ones launched in the background, ones launched through a shell wrapper, and
ones whose job reported failure but left a child alive. Name what you start
and stop it by that name.

Two reasons, both measured rather than assumed:

- A leftover process is invisible. A dev server left polling every four
  seconds, and one benchmark that outlived its own job, made a single import
  measure 41 s alone and 983 s beside them. The wrong numbers were plausible
  enough to act on.
- Anything the *user* started is not yours to kill. Identify a process by
  command line and start time before touching it.

Corollary for benchmarks and timings: check what is still running before
measuring, and never run two measurements at once. A measurement taken beside
other work is not a measurement.

## Iteration discipline

1. *(default)* Work in small vertical slices - a working increment beats a big-bang
   branch.
2. *(rule)* Failed fix attempts: 3 strikes -> stop, revert to last known good,
   re-analyze before another change. No shotgun debugging.
3. *(default)* Deprecation path for replaced functionality: mark deprecated ->
   migrate users/data -> delete in a later commit ([naming
   discipline](03-project-structure.md):
   no `_v2` twins living forever).
4. *(default)* One plan, one working session. When work has to cross into
   another release, application, or problem class, hand off instead of
   continuing; long sessions erode scope faster than they save time. Git
   history records *what changed*, not *what was decided or still open*, so
   it is not a substitute for a plan
   ([planning](21-planning.md#one-plan-one-session-default)).
5. *(rule)* Deterministic first, AI second: if a problem is solvable reliably with parsing, rules, APIs, SQL, state machines, conventional code, or a CLI, use that first. Use a model only where interpretation, classification, fuzzy matching, extraction, summarization, or reasoning is required.
6. *(default)* AI-optional applications: core workflows must remain functional without an LLM stack (improves offline longevity, local testing, and cost control).
