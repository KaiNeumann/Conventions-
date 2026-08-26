# AGENTS.md - <Project Name>

Rules for AI agents working in this repository. Copy this file into a
project, fill every `<placeholder>`, delete the guidance comments - then
keep it under 200 lines. Humans benefit from the same discipline.

Conventions baseline: <conventions repository> v<version> - see its `CHANGELOG.md`.

## Safety gates (non-negotiable)

Read these before doing anything else. Violating one means stop and ask,
even mid-task.

- Never access credentials, secret stores, or vaulted content without
  explicit human approval - even when a task seems to require it.
- Never run destructive commands (deleting data, dropping tables,
  force-pushing, resetting environments) unless explicitly requested.
- <project-specific gates - network policies, payment restrictions,
  data-classification limits>

## Automation contract

Every push triggers CI (<workflow name>).

- Do **not** pre-run the full test suite on routine changes:
  commit -> push -> read the CI result.
- Local full runs only when debugging a red pipeline
  (`<check command>`).
- If CI fails: fix the root cause named in the failing step's log tail,
  push again. Never weaken tests, hooks, or workflows to get green.

## Global rules

- OS/shell: <Windows + PowerShell | Linux + bash>. Paths via
  `pathlib.Path` / `Join-Path`, never hardcoded absolute paths.
- All text IO with explicit `encoding="utf-8"`; never rely on system
  codepages.
- Disposable artifacts go to `temp/` (gitignored) - never into the home
  directory.
- Use the repo-local environment (<venv path>) if present.
- Testing policy: <deterministic offline tests | live-network allowed
  for ...>.

## Architecture pointers

- <What lives where: canonical packages/modules, entry points.>
- <Deprecated or frozen zones - do not build on them.>
- Canonical commands: check `<command>`, run `<command>`, package
  `<command>`.

## Known gotchas

<Hard-won traps, each as wrong/right example pair - quoting issues,
line endings, encoding, ordering constraints. Delete section if empty.>

## Privacy

- No usernames, account names, or personal data in commits, issues,
  logs, or examples - use `<user>` placeholders even when quoting logs.
- Settings and credentials follow <link to project settings docs>;
  never plaintext secrets in the repo.

## Prohibited without explicit instruction

- Editing files outside the declared task scope
- Committing or pushing unrelated changes found in the worktree
- Introducing new dependencies without documenting why in the task
