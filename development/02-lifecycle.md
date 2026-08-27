---
title: Development Lifecycle
type: reference
tags: [conventions, development, process]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Development Lifecycle

## Stages (default)

```
idea → plan → implement → verify → document → commit → deploy
```

1. **Idea** - capture it (issue or `TODO-backlog.md`), one line is enough.
   Don't build it yet.
2. **Plan** - for anything beyond a trivial fix: bullet list of steps +
   acceptance criteria in the issue/TODO item. Agents state the plan
   before touching code.
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

## Definition of done (rule)

A task is done when ALL are true:

- [ ] Code works as specified (verified by running it, not assumed)
- [ ] Tests exist for new logic; suite green via CI (locally only when
      the repo has no pipeline)
- [ ] Lint/type checks clean on touched files
- [ ] Docs updated where they became wrong
- [ ] No secrets/local artifacts staged
- [ ] Committed per [git conventions](01-git.md)

(Small scripts and one-off tools may deliberately skip tests/docs -
say so, don't silently skip.)

## Iteration discipline

1. *(default)* Work in small vertical slices - a working increment beats a big-bang
   branch.
2. *(rule)* Failed fix attempts: 3 strikes -> stop, revert to last known good,
   re-analyze before another change. No shotgun debugging.
3. *(default)* Deprecation path for replaced functionality: mark deprecated ->
   migrate users/data -> delete in a later commit ([naming
   discipline](03-project-structure.md):
   no `_v2` twins living forever).
4. *(default)* Keep a session log only when work spans sessions - otherwise git
   history IS the log.
5. *(rule)* Deterministic first, AI second: if a problem is solvable reliably with parsing, rules, APIs, SQL, state machines, conventional code, or a CLI, use that first. Use a model only where interpretation, classification, fuzzy matching, extraction, summarization, or reasoning is required.
6. *(default)* AI-optional applications: core workflows must remain functional without an LLM stack (improves offline longevity, local testing, and cost control).
