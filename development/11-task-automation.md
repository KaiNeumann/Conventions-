---
title: Task Automation and CI
type: reference
tags: [conventions, development, ci, automation]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Task Automation and CI

Running tests, building the app, and verifying after every commit is
infrastructure work, not intelligence work. Each hand-executed loop burns
LLM tokens on the exact same steps. Automation removes it from the model's
context entirely.

## Principle (rule)

Recurring post-commit tasks are automated infrastructure. When automation
exists for a repo, agents **MUST NOT** hand-run the full verify loop on
routine commits: commit → push → read failure summaries. Hand-running the
suite is for debugging a failure or when no automation exists yet.

## Three layers

### 1. Task entry point (default)

Every project exposes **one canonical command** that runs lint + tests +
build — for example `tools/check.py`, `just check`, or `make check`.

- Humans, git hooks, CI workflows, and agents all call the same command;
  nothing improvises multi-step loops.
- Flavor per project is free; Python-based `tools/check.py` is the most
  portable given our Windows-first reality (no make/WSL dependency).
- The command exits non-zero on any failure and prints a short summary —
  designed so an agent can act on the tail of the output alone.

### 2. Local pre-push hook (default)

Committed under `.githooks/`, activated once per clone:

```bash
git config core.hooksPath .githooks
```

`.githooks/pre-push` calls the task entry point; a non-zero exit blocks
the push. Broken code never reaches the remote.

- Hook scripts are Python or PowerShell — no bash-only constructs
  (Windows-first rule from [`09-cross-platform.md`](09-cross-platform.md)).
- Hooks are advisory-by-nature (`--no-verify` exists); the authoritative
  gate is layer 3. Bypassing a hook requires explicit human instruction.
- Mention activation in the repo README (one line), since clones don't
  inherit `core.hooksPath`.

### 3. Server-side gate (default for repos with a remote)

Self-hosted **Forgejo Actions** on `git.kaiuweneumann.de`: workflows in
`.forgejo/workflows/*.yml`, executed by the runner on vishnu (runner runs
on vishnu because every push already requires vishnu online — no extra
availability machinery; see the 2026-homeserver design doc,
`docs/2026-setup`, "Forgejo Actions & Runner").

- Repos hosted on Codeberg use Codeberg's hosted CI instead — same
  workflow syntax, no self-hosted runner needed.
- Workflows call the same task entry point as layer 1 — one definition of
  "verified", three consumers.

Workflow template:

```yaml
on: [push]
jobs:
  test:
    runs-on: python-ci        # label provided by the vishnu runner
    strategy:
      matrix:
        python: ["3.11", "3.13"]
    steps:
      - uses: https://data.forgejo.org/actions/checkout@v4
      - run: pip install -e '.[dev]' && tools/check.py
```

## Agent rules (rule)

1. Commit → push → read the CI result. Do not pre-run what CI will run.
2. On CI failure: read the *failing step's* log tail, fix the root cause,
   push again. No local full-suite re-runs "to be sure".
3. Never commit disabled/broken pipelines to make CI green — fix or
   explicitly mark the workflow excluded with a reason.
4. Setting up layers 1–2 in a new repo is part of repo bootstrap
   ([`04-repo-standard-files.md`](04-repo-standard-files.md)) once the
   project has anything worth testing.

## Rationale

Token math: today each commit costs an agent-run pytest/build/push loop —
identical output read into context every single time. With the three
layers, the steady-state cost per commit collapses to two commands plus
failure handling, and the authoritative verification happens outside the
model entirely.
