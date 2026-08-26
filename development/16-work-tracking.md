---
title: Work Tracking
type: reference
tags: [conventions, development, todos]
status: accepted
created: 2026-08-25
updated: 2026-08-25
---

# Work Tracking

Known bugs, open issues, and todos live where humans **and** agents can
see them without special access: an in-repo tracking file, backed by
remote issues once a project outgrows it.

## Surfaces *(default)*

| Surface | Use |
|---|---|
| `TODO.md` at repo root | Canonical queue: known bugs, todos, ideas. Agent-readable by definition |
| Remote issues (Forgejo/Codeberg/GitHub) | Public reports, discussion history, cross-machine visibility. Summarize back into `TODO.md` so agents stay informed |
| `CHANGELOG.md` | Fixed items get announced here at release, then leave the queue |

Never maintain divergent detail in both places: the remote issue holds
the discussion, `TODO.md` holds the current state, one link connects
them.

**Promotion rule** *(default)*: an item moves from `TODO.md` to a
remote issue only when it needs public reporting or durable
discussion - and even then `TODO.md` keeps a one-line pointer to the
issue instead of the details.

## File structure *(default)*

```markdown
# TODO

## Bugs

- **[P1][BUG] Upload stalls above 2 GiB - OPEN**
  Repro: queue two 3 GiB files over Tor. Expected: sequential run.
  Actual: second task stays RUNNING forever. Workaround: none.
  Suspect: stream buffer reuse. Refs: src/transfer/queue.py

## Todos

- **[P2] Retry failed upload on fresh session - IN PROGRESS**
  Done when: a failing upload retries once with a new session id and
  the test suite covers it. Refs: tests/test_retry.py

## Ideas

- **Export archive manifest as RSS** (unrefined - no criteria yet)
```

## Entry anatomy *(rule)*

**Shared headline format** - TODO entries and remote issue titles use
the same shape, so scanning either surface feels identical:

```
[P<priority>][<kind>][<area>] Imperative summary
```

Example: `[P1][BUG][transfer] Upload stalls above 2 GiB`

1. Tags up front: priority `[P1]` ship-blocker / `[P2]` should-fix /
   `[P3]` nice-to-have is required; **kind** (`BUG`, `FEATURE`, `DOCS`,
   ...) and **area** (component, module, or top-level folder - e.g.
   `transfer`, `wiki`, `cli`) are optional and must stay consistent per
   repo. Area values mirror the repository's own structure so filtering
   by folder comes for free.
2. Imperative summary - stable across the item's life; never reworded
   to express status.
3. Status differs per surface: TODO entries append it to the headline
   (`- OPEN`, `- IN PROGRESS`, `- BLOCKED`, `- DONE`, `- REJECTED`);
   remote issues carry status natively via labels/issue state.
4. A body that answers the three cold-start questions - the ones every
   fresh agent session would otherwise ask:
   - What exactly is broken / to be built? (repro steps or scope)
   - When is it done? (*Done when:* criteria)
   - Where does the work land? (file/module refs)

Terminal statuses are `DONE` and `REJECTED`; both move to the Archive
tail instead of being deleted.

## Rules

1. **Capture beats forgetting** *(default)* - deferring work means
   adding one entry line immediately, then continuing the current task.
2. **Agents keep entries alive** *(rule)* - update status and findings
   while working; close with a one-line resolution. Entries are never
   deleted silently; `DONE` items move to an Archive tail and rot out
   with releases.
3. **Humans prune** *(default)* - if live items exceed ~20, split,
   defer, or promote to remote issues. A queue nobody reads is worse
   than none.
