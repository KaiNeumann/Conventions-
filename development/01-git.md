---
title: Git Conventions
type: reference
tags: [conventions, development, git]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Git Conventions

## Remotes and hosting (default)

1. Default host: self-hosted **Forgejo** or
   Codeberg; public projects may mirror to GitHub. Any other host is
   fine when the project calls for it — this is the default, not a rule.
2. Git operations use **SSH**, not HTTPS where the host supports it
   (HTTPS often sits behind auth portals).
3. Default branch: `main`.

## Commits

1. *(rule)* Small, atomic commits: one logical change that leaves the repo working.
2. *(default)* Message format:

   ```
   <type>: imperative summary, max ~72 chars

   Optional body explaining why (not what).
   ```

   Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`.
3. *(rule)* **Before every commit, run `git status --short --ignored`** and review
   what is staged. Never commit: secrets, tokens, `.env`, local agent
   state (`.tmp/`, `.sisyphus/`, `.playwright-mcp/`), build output,
   venvs, databases/SQLite files.
4. *(rule)* Pushed history on shared `main` is immutable — fix forward.
   **Solo exception:** when working alone you may rewrite your own
   pushed `main` with `--force-with-lease` (never plain `--force`),
   provided no other machine has pulled recently.
5. *(default)* No AI-attribution trailers (`Co-authored-by:` naming an
   agent, "generated with…" footers). Commit messages stay minimal;
   authorship is visible through git author config alone.

## Branching (default)

1. Solo projects: trunk-based — commit to `main`, branch only for risky
   or experimental work (`feat/<topic>`, `experiment/<name>`).
2. Merge branches with regular merge commits or fast-forward; no stacked
   mystery history. Delete branches after merge.

## Cross-platform hygiene (rule)

1. Commit with LF (`end_of_line = lf` via `.editorconfig`,
   `.gitattributes` for text=auto). Do not "fix" line-ending churn from
   WSL/Windows index normalization by staging it — leave those files out
   of unrelated pushes (established repo rule).
2. Windows worktree is primary; WSL is used deliberately (e.g. SSH git),
   not accidentally.

## Issues and housekeeping

1. *(default)* Use Forgejo/Codeberg issues for TODOs that outlive a
   session; keep a short `TODO-backlog.md` in-repo for agent-visible
   work items.
2. *(rule)* **No personal data, no usernames** in issue titles, bodies,
   comments, or quoted logs — use `<user>` placeholders.
3. *(rule)* API tokens for issue tooling come via `--token-file`, never
   env vars, never hardcoded paths.
