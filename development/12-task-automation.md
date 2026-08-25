---
title: Task Automation and CI
type: reference
tags: [conventions, development, ci, automation]
status: accepted
created: 2026-08-23
updated: 2026-08-24
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

### 2. Local pre-push hook (optional)

Committed under `.githooks/`, activated once per clone:

```bash
git config core.hooksPath .githooks
```

`.githooks/pre-push` calls the task entry point; a non-zero exit blocks
the push. Broken code never reaches the remote.

- Optional infrastructure, not a default: adopt where early local
  feedback is worth the setup; the Forgejo gate (layer 3) remains the
  authoritative check either way.
- Hook scripts are Python or PowerShell — no bash-only constructs
  (Windows-first rule from [`10-cross-platform.md`](10-cross-platform.md)).
- Hooks are advisory-by-nature (`--no-verify` exists). Bypassing a hook
  requires explicit human instruction.
- Repos that ship hooks MUST document activation in their README (one
  line), since clones don't inherit `core.hooksPath`.

### 3. Server-side gate (default for repos with a remote)

The self-hosted **Forgejo** instance runs Actions: workflows in
`.forgejo/workflows/*.yml`, executed by a self-hosted runner placed on
the same host as the forge: every push already requires that host
online (git SSH), so no extra availability machinery is needed.
Deployment design lives with the infrastructure repository.

- Repos hosted on Codeberg use Codeberg's hosted CI instead — same
  workflow syntax, no self-hosted runner needed.
- Workflows call the same task entry point as layer 1 — one definition of
  "verified", three consumers.

Workflow template:

```yaml
on: [push]
jobs:
  test:
    runs-on: python-ci        # label provided by your registered runner
    steps:
      - uses: https://data.forgejo.org/actions/checkout@v4
      - run: pip install -e '.[dev]' && tools/check.py
      # add a strategy.matrix over Python versions only when a repo
      # actually supports multiple versions
```

### Verification contract in AGENTS.md (rule)

A repo that enables a CI workflow **MUST** state its automation contract
in `AGENTS.md` — at minimum: *pushes trigger CI; agents do not pre-run
the full suite on routine changes; failures are fixed from the failing
step's log tail.* Keep this wording identical across repositories so agents can rely on it. Without this note, agents default to hand-running
everything and the token savings never materialize.

## Packaging entry point (strong recommendation)

Projects that produce artifacts (executables, images) **SHOULD** expose
one canonical package command — for example `tools/package.py` wrapping
the real builder:

```bash
python tools/package.py   # = pyinstaller --noconfirm markview.spec
```

1. The build recipe lives in tracked spec files (`markview.spec`,
   `Dockerfile`); nobody improvises builder flags on the command line,
   humans and agents included.
2. While no artifact pipeline exists yet (see Open decisions), this
   command **is** the build interface for manual and agent-driven builds.
3. When tag-gated CI builds arrive, they call the same command — one
   definition of "built", like layer 1 is one definition of "verified".
4. Prerequisites that CI does not need (e.g. `pyinstaller`) are installed
   on demand and documented in the repo's `AGENTS.md`, keeping per-push
   CI installs lean.

## Agent rules (rule)

1. Commit → push → read the CI result. Do not pre-run what CI will run.
2. On CI failure: read the *failing step's* log tail, fix the root cause,
   push again. No local full-suite re-runs "to be sure".
3. Never commit disabled/broken pipelines to make CI green — fix or
   explicitly mark the workflow excluded with a reason.
4. Setting up layers 1–2 in a new repo is part of repo bootstrap
   ([`04-repo-standard-files.md`](04-repo-standard-files.md)) once the
   project has anything worth testing.

## Open decisions

1. *(planned default)* **Artifact builds vs tests:** tests run on every
   push; artifact builds (Docker images, binaries) run only on version
   tags (`v*`) or explicit trigger — never per-push, never in the hot
   path.
2. *(planned)* **Windows .exe strategy:** target is Wine-based
   cross-builds on a **Linux** runner (Docker + Wine, an approach
   `tools/build/package.py --win`), so producing Windows binaries never
   depends on owning a Windows machine — deliberate given the planned
   migration away from Windows. Native Windows runners are not planned
   unless cross-builds prove impractical.
3. *(interim accepted)* While an app is unstable and needs executables
   for frequent manual testing, building locally on the dev desktop via
   the project's canonical package command is fine — the runner takeover
   happens once the build recipe is proven.

## Rationale

Token math: today each commit costs an agent-run pytest/build/push loop —
identical output read into context every single time. With the three
layers, the steady-state cost per commit collapses to two commands plus
failure handling, and the authoritative verification happens outside the
model entirely.
