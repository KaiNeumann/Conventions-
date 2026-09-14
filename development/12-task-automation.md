---
title: Task Automation and CI
type: reference
tags: [conventions, development, ci, automation]
status: accepted
created: 2026-08-23
updated: 2026-09-14
---

# Task Automation and CI

Running tests, building the app, and verifying after every commit is
infrastructure work, not intelligence work. Each hand-executed loop burns
LLM tokens on the exact same steps. Automation removes it from the model's
context entirely.

## Principle (rule)

Recurring post-commit tasks are automated infrastructure. When automation
exists for a repo, agents **MUST NOT** hand-run the full verify loop on
routine commits: commit -> push -> read failure summaries. Hand-running the
suite is for debugging a failure or when no automation exists yet.

Automate repeatable mechanics such as checks, file moves, downloads, and
condition checks. Keep ambiguous classification or consequential decisions
visible until there is evidence to express them as deterministic policy.

## Three layers

### 1. Task entry point (default)

Every project exposes **one canonical command** that runs lint + tests +
build - for example `tools/check.py`, `tools/check.ps1`, `just check`, or
`make check`.

- Humans, git hooks, CI workflows, and agents all call the same command;
  nothing improvises multi-step loops.
- Flavor per project is free. Python-based `tools/check.py` is preferred
  when portability matters, but Windows-first repositories may use
  `tools/check.ps1` or `build.ps1` as their canonical command. Their CI
  runner must support the selected command.
- The command exits non-zero on any failure and prints a short summary -
  designed so an agent can act on the tail of the output alone.

### Indentation-sensitive validation *(rule)*

Supported indentation-sensitive source and configuration formats **MUST**
be validated deterministically through the canonical project check command.
Use an appropriate formatter check, parser, compiler, or linter. Visual
review, editor formatting, agent harnesses, plugins, skills, and LLM review
do not count as validation.

YAML validation **MUST** parse the files and enforce checked-in project
policy. Frontmatter **MUST** satisfy the schema owned by its project or
document set. Any validation failure **MUST** make the canonical check
command exit non-zero.

The shared validation CLI is the default implementation. Pin it through the
project's normal development-tool mechanism, commit its policy, and invoke it
from the canonical check command on every supported local and CI platform.
Projects **MUST NOT** depend on a global installation.

#### Templates that emit structured output *(rule)*

Templates (Jinja2, ERB, Go templates, ...) that generate YAML, JSON, TOML,
or similar carry a stricter obligation than hand-written files, because a
template can parse cleanly and still be structurally wrong: a one-space
indent shift can silently demote a section into the previous section's
item list, merge groups, or drop entries while remaining valid YAML.

1. **Read before reformatting.** Before touching whitespace, indentation,
   or block structure in a template, the agent **MUST** inspect the
   original bytes (`git show HEAD:<path>` or the pre-edit file). Templates
   are not prose: the existing indentation is load-bearing, and "looks
   misaligned" is not evidence of an error.
2. **Baseline render before structural edits.** Before an edit that can
   change emitted structure, render the template with representative
   variables and keep the parsed result.
3. **Structural diff after editing.** After editing, re-render with the
   same variables and compare the *parsed structures*: same top-level
   keys/sections in the same order, same membership of lists/groups.
   Parseability alone does not validate a template edit.
4. **Expected-absence is failure.** When a validation or render output
   lacks an element the pre-edit version had (a section, key, card, or
   entry), that is a failure signal. Agents **MUST NOT** log such output
   as success or continue past it.
5. **Encode the check.** Where a template feeds a long-lived surface
   (dashboard config, compose files, routing config), the structural
   comparison **SHOULD** live as a repo test so future edits are gated
   deterministically.

Rationale: a real incident rendered a dashboard config that parsed
cleanly while an entire server group had been folded into another group's
item list, because the "fix" for a parse error re-indented a section
header without reading the original and validation only asserted
parseability. Cost: repeated deployments, user-visible breakage, and a
full debug cycle. All three failure points above were present and each
alone would have prevented it.

### CLI before MCP (default)

When an application capability needs to be used by people, scripts, or
agents, expose a documented CLI before adding an MCP server. A CLI is
discoverable, scriptable, testable, and token-efficient. Add MCP only when
its tool discovery or session semantics provide a concrete benefit; it calls
the same underlying capability rather than owning separate logic.

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
- Hook scripts are Python or PowerShell - no bash-only constructs
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

- Repos hosted on Codeberg use Codeberg's hosted CI instead - same
  workflow syntax, no self-hosted runner needed.
- Workflows call the same task entry point as layer 1 - one definition of
  "verified", three consumers.

Workflow template:

```yaml
on: [push]
jobs:
  test:
    runs-on: python-ci        # label provided by your registered runner
    steps:
      - uses: https://data.forgejo.org/actions/checkout@v4
      - run: pip install -e '.[dev]' && tools/check.py # or pwsh -File tools/check.ps1
      # add a strategy.matrix over Python versions only when a repo
      # actually supports multiple versions
```

### Verification contract in AGENTS.md (rule)

A repo that enables a CI workflow **MUST** state its automation contract
in `AGENTS.md` - at minimum: *pushes trigger CI; agents do not pre-run
the full suite on routine changes; failures are fixed from the failing
step's log tail.* Keep this wording identical across repositories so agents can rely on it. Without this note, agents default to hand-running
everything and the token savings never materialize.

## Windows cross-build strategy (default)

Windows executables are produced via **Wine-based cross-builds on a
Linux runner** (Docker + Wine, `tools/build/package.py --win`), so
producing Windows binaries never depends on owning a Windows machine -
deliberate given the planned migration away from Windows. Native
Windows runners are not planned unless cross-builds prove impractical;
if Wine-based PyInstaller turns out to be too fragile in practice, fall
back to a native Windows runner rather than silently shipping broken
builds. This is the one story the packaging docs tell consistently:
[`09-packaging-desktop.md`](09-packaging-desktop.md) (cross-builds via
Docker), [`10-cross-platform.md`](10-cross-platform.md) (cross-compilation
as a default).

## Packaging entry point (strong recommendation)

Projects that produce artifacts (executables, images) **SHOULD** expose
one canonical package command - for example `tools/package.py` wrapping
the real builder:

```bash
python tools/package.py   # = pyinstaller --noconfirm markview.spec
```

1. The build recipe lives in tracked spec files (`markview.spec`,
   `Dockerfile`); nobody improvises builder flags on the command line,
   humans and agents included.
2. While no artifact pipeline exists yet (see Open decisions), this
   command **is** the build interface for manual and agent-driven builds.
3. When tag-gated CI builds arrive, they call the same command - one
   definition of "built", like layer 1 is one definition of "verified".
4. Prerequisites that CI does not need (e.g. `pyinstaller`) are installed
   on demand and documented in the repo's `AGENTS.md`, keeping per-push
   CI installs lean.

## Agent rules (rule)

1. Commit -> push -> read the CI result. Do not pre-run what CI will run.
2. On CI failure: read the *failing step's* log tail, fix the root cause,
   push again. No local full-suite re-runs "to be sure".
3. Never commit disabled/broken pipelines to make CI green - fix or
   explicitly mark the workflow excluded with a reason.
4. Setting up layers 1-2 in a new repo is part of repo bootstrap
   ([`04-repo-standard-files.md`](04-repo-standard-files.md)) once the
   project has anything worth testing.

## Open decisions

1. *(planned default)* **Artifact builds vs tests:** tests run on every
   push; artifact builds (Docker images, binaries) run only on version
   tags (`v*`) or explicit trigger - never per-push, never in the hot
   path.
2. *(interim accepted)* While an app is unstable and needs executables
   for frequent manual testing, building locally on the dev desktop via
   the project's canonical package command is fine - the runner takeover
   happens once the build recipe is proven.

## Rationale

Token math: today each commit costs an agent-run pytest/build/push loop -
identical output read into context every single time. With the three
layers, the steady-state cost per commit collapses to two commands plus
failure handling, and the authoritative verification happens outside the
model entirely.
