---
title: Language Standards
type: reference
tags: [conventions, development, languages]
status: accepted
created: 2026-08-23
updated: 2026-08-23
---

# Language Standards

Everything in this file is **default** — the stack we start new projects
with. Deviate freely when the project calls for it; note the deviation in
the project README/AGENTS.md. The inline *(rule)* tags mark the few
portability/safety points that bind everywhere.

## Python (default for tools, backends, CLIs, GUIs)

1. **Version**: current stable as floor (`requires-python = ">=3.11"`),
   build/bundle on the exact minor used in production images (e.g. 3.12).
2. **Packaging**: `pyproject.toml` only, once a project is packaged —
   unpackaged stdlib micro apps are exempt until then
   ([`03-project-structure.md`](03-project-structure.md) flat-root
   allowance). Backends seen in practice:
   hatchling (libraries/apps) or setuptools (monorepos). Pick one per
   repo.
3. **Dependencies**: ranged pins `>=x.y,<next-major`. Extras groups:
   `dev` (pytest, linters, build), plus optional runtime extras (`web`,
   `ui`, `ocr`, …) so base installs stay lean.
   *(rule)* **Declared dev dependencies** — test/dev tooling lives in
   tracked files (`requirements-dev.txt`, `[dev]` extra); pipelines
   install from tracked files only, never ad-hoc installs in CI steps.
4. **Layout**: `src/` layout, pytest with `testpaths` configured in
   pyproject. Repo-local `.venv` for runs (use the repo venv if present).
5. **Stack choices** (proven in this workspace):
   - CLI: `typer`
   - HTTP API: `fastapi` + `uvicorn`
   - Data/models: `pydantic`
   - Config: YAML/INI persisted settings files over env vars (env vars
     only for container wiring/tests)
6. **Quality gates**: ruff (lint+format), pytest; type hints required on
   public APIs.
7. *(rule)* **Text handling**: explicit `encoding="utf-8"` on all file IO;
   never rely on the Windows ANSI codepage. ASCII default unless content
   needs Unicode.

## TypeScript / frontend

1. **Default**: React + Vite + Tailwind CSS, strict `tsconfig`
. Pinned exact versions in `package.json`.
2. **Offline/small tools**: vendored zero-build static SPA (Markview
   pattern) — no CDN, no required build step, dependencies committed
   under `vendor/`.
3. Scripts every frontend must define: `dev`, `build`, `preview`, `test`.
4. No `any` suppression of type errors; no `@ts-ignore`.

## Shell / automation

1. PowerShell on Windows (no bash-isms); explicit `-Encoding utf8`;
   `Join-Path`/`Resolve-Path`/`pathlib.Path` over string-concatenated
   paths.
2. Bash for Linux/server scripts; POSIX-compatible unless bash features
   are needed.
3. Ansible for infrastructure provisioning;
   day-2 ops changes flow back into playbooks, not hand-edits.

## Choosing a language (default)

1. Script/tool/backend/GUI → Python.
2. Browser UI → TypeScript (React/Vite) or zero-build vanilla JS for
   offline tools.
3. Everything else → justify in the project README before starting.
