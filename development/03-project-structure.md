---
title: Project Structure
type: reference
tags: [conventions, development, structure]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Project Structure

Layouts below are the **default for new projects**; existing projects
adopt them when convenient. The naming discipline at the end is a rule.

## Python application/service (default)

```
project/
â”œâ”€â”€ src/<package>/        # all application code (src layout, import as src.<package>â€¦)
â”œâ”€â”€ tests/                # pytest suite (unit + integration subfolders when large)
â”œâ”€â”€ docs/                 # architecture notes, howtos, decision records
â”œâ”€â”€ tools/                # dev/build scripts (packaging, codegen, housekeeping)
â”œâ”€â”€ data/                 # runtime data â€” gitignored
â”œâ”€â”€ pyproject.toml        # single source of truth: deps, entry points, pytest config
â”œâ”€â”€ README.md
â”œâ”€â”€ AGENTS.md             # when agents work here (see documentation conventions)
â”œâ”€â”€ .gitignore / .dockerignore / .editorconfig
â”œâ”€â”€ Dockerfile            # when deployable
â””â”€â”€ docker-compose.yml    # when it has services/state
```

- Entry points via `[project.scripts]`; runnable as module too
  (`python -m <package>`).
- Version lives once in code (`dynamic = ["version"]` /
  `attr = "<pkg>.constants.VERSION"`), not hand-edited in five places.
- `README.md` / `AGENTS.md` content per
  [`06-documentation.md`](06-documentation.md); the standard dotfiles
  come from [`04-repo-standard-files.md`](04-repo-standard-files.md).
- House spelling is `tests/` (plural); existing `test/` dirs rename
  whenever convenient, no forced churn.
- Tracked empty dirs use the gitkeep pattern: ignore `data/*`, keep
  `!data/.gitkeep`.

## Frontend / fullstack (default)

```
frontend/  (or backend/ + frontend/)
â”œâ”€â”€ src/                  # React/Vite source
â”œâ”€â”€ tests/ or e2e/        # Playwright smoke tests
â”œâ”€â”€ package.json          # pinned deps, npm scripts: dev / build / test
â””â”€â”€ vite.config.ts
```

Fullstack splits backend/frontend into sibling folders (ScraperCMS
pattern), each with its own dev commands documented in README.

## Monorepo (multiple apps sharing a core) (pattern)

Pattern from RAT; adopt when a repo really has multiple apps sharing
code.

```
repo/
â”œâ”€â”€ src/shared/           # canonical shared namespace (imports: src.shared.*)
â”œâ”€â”€ src/<app>/            # one folder per app
â”œâ”€â”€ adapters|plugins_ext/ # external overlay plugins, loaded without patching core
â”œâ”€â”€ packaging/<app>/      # per-app PyInstaller specs
â””â”€â”€ tools/build/          # canonical packager
```

Rules (from RAT):
1. One canonical import namespace (`src.shared.runtime.*`); legacy
   namespaces are unsupported â€” never reintroduce aliases.
2. Overlay/external plugin folders override specific namespaces only â€”
   no global `sys.path` hacks.

## Growth rule (default)

Start simple â€” stdlib-only micro apps **may** keep entry modules at
repo root (markdownviewer, organizer pattern). Move into `src/` once a
second module or packaging appears; split into the standard layout when
two top-level concerns exist. Promote structure when it hurts â€” don't
pre-build empty scaffolding.

## Naming discipline (rule)

No vague suffixes in anything new: `_v2`, `_new`, `_enhanced`, `_direct`,
`_final`. Names state responsibility: `f95zone_story.py`, not
`f95zone_story_enhanced.py`. Replaced code gets deprecated and deleted,
not suffixed.
