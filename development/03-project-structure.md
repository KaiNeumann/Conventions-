---
title: Project Structure
type: reference
tags: [conventions, development, structure]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Project Structure

Layouts below are the **default for new projects**; existing projects
adopt them when convenient. The naming discipline at the end is a rule.

## Python application/service (default)

```
project/
├── src/<package>/        # all application code (src layout, import as src.<package>…)
├── tests/                # pytest suite (unit + integration subfolders when large)
├── docs/                 # architecture notes, howtos, decision records
├── tools/                # dev/build scripts (packaging, codegen, housekeeping)
├── data/                 # runtime data — gitignored
├── pyproject.toml        # single source of truth: deps, entry points, pytest config
├── README.md
├── AGENTS.md             # when agents work here (see documentation conventions)
├── .gitignore / .dockerignore / .editorconfig
├── Dockerfile            # when deployable
└── docker-compose.yml    # when it has services/state
```

- Entry points via `[project.scripts]`; runnable as module too
  (`python -m <package>`).
- Version lives once in code (`dynamic = ["version"]` /
  `attr = "<pkg>.constants.VERSION"`), not hand-edited in five places.
- `README.md` / `AGENTS.md` content per
  [`06-documentation.md`](06-documentation.md); the standard dotfiles
  come from [`04-repo-standard-files.md`](04-repo-standard-files.md).

## Frontend / fullstack (default)

```
frontend/  (or backend/ + frontend/)
├── src/                  # React/Vite source
├── tests/ or e2e/        # Playwright smoke tests
├── package.json          # pinned deps, npm scripts: dev / build / test
└── vite.config.ts
```

Fullstack splits backend/frontend into sibling folders (ScraperCMS
pattern), each with its own dev commands documented in README.

## Monorepo (multiple apps sharing a core) (pattern)

Pattern from RAT; adopt when a repo really has multiple apps sharing
code.

```
repo/
├── src/shared/           # canonical shared namespace (imports: src.shared.*)
├── src/<app>/            # one folder per app
├── adapters|plugins_ext/ # external overlay plugins, loaded without patching core
├── packaging/<app>/      # per-app PyInstaller specs
└── tools/build/          # canonical packager
```

Rules (from RAT):
1. One canonical import namespace (`src.shared.runtime.*`); legacy
   namespaces are unsupported — never reintroduce aliases.
2. Overlay/external plugin folders override specific namespaces only —
   no global `sys.path` hacks.

## Growth rule (default)

Start simple (a small app may be one module under `src/`), but the moment
there are two top-level concerns, split into the standard layout above.
Promote structure when it hurts — don't pre-build empty scaffolding.

## Naming discipline (rule)

No vague suffixes in anything new: `_v2`, `_new`, `_enhanced`, `_direct`,
`_final`. Names state responsibility: `f95zone_story.py`, not
`f95zone_story_enhanced.py`. Replaced code gets deprecated and deleted,
not suffixed.
