---
title: Development Conventions
type: reference
tags: [conventions, development]
status: accepted
created: 2026-08-23
updated: 2026-08-23
---

# Development Conventions

How we build software — for humans and AI agents.

Sections are tiered per [`../README.md`](../README.md): **(rule)** binds
everywhere, **(default)** applies to new projects unless noted otherwise,
**(pattern)** is a proven solution to copy when useful. Most of this area
is defaults — the rules are the few things that prevent data loss,
security holes, or agent damage.

This area is reference documentation — verbose where it aids
understanding. Terse agent-loading distillations are derived artifacts,
extracted from here (see [`../README.md`](../README.md), "Purpose").

## Reading order

1. [`01-git.md`](01-git.md) — git usage, remotes, commits
2. [`02-lifecycle.md`](02-lifecycle.md) — from idea to shipped, definition of done
3. [`03-project-structure.md`](03-project-structure.md) — standard layout (`src/`, `tests/`, docs)
4. [`04-repo-standard-files.md`](04-repo-standard-files.md) — `.gitignore`, `.dockerignore`, `.editorconfig` templates
5. [`05-languages.md`](05-languages.md) — per-language standards (Python, TypeScript, …)
6. [`06-documentation.md`](06-documentation.md) — README, AGENTS.md, inline comments, decision records
7. [`07-packaging-web.md`](07-packaging-web.md) — Dockerized web apps
8. [`08-packaging-desktop.md`](08-packaging-desktop.md) — native desktop GUIs (pywebview/Tkinter, PyInstaller)
9. [`09-cross-platform.md`](09-cross-platform.md) — portability rules for all delivery modes
10. [`10-ci.md`](10-ci.md) — CI and release pipelines
11. [`11-task-automation.md`](11-task-automation.md) — token-saving automation: task entry point, pre-push hook, Forgejo Actions gate
12. [`12-licensing.md`](12-licensing.md) — license selection by repo category, SPDX mechanics, target state for existing repos
13. [`13-gui-design.md`](13-gui-design.md) — GUI principles, visual tokens, keyboard-first interaction, accessibility baseline
14. [`14-logging.md`](14-logging.md) — log location, entry format, filterable identifiers, noise control
15. [`15-settings.md`](15-settings.md) — settings location (portable sidecar vs profile), resilience, sensitive-value encryption, one settings truth

## Core principles

- **Boring and reproducible.** Standard layouts, standard tools, pinned
  versions. A stranger (or agent) must be productive in minutes.
- **One core, many shells.** Business logic lives in a library core;
  desktop GUI, CLI, and web UI are thin shells over it (RAT pattern).
- **Docker-first for anything with a UI or service**; native desktop apps
  where a desktop makes sense — same frontend, different shell.
- **Agent-safe by construction.** Repos carry `AGENTS.md`, safety gates,
  and deterministic tests so agents can work without breaking things.
- **Secrets never enter git.** Vaulted, env-file examples, or secret files
  outside the repo.
