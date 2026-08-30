---
title: Packaging - Native Desktop Apps
type: reference
tags: [conventions, development, packaging]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Packaging - Native Desktop Apps

For when a desktop app makes sense. One part of the "one core, many
shells" model - the same core also ships as web app
([`08-packaging-web.md`](08-packaging-web.md)) and usually a headless CLI
(see [`05-languages.md`](05-languages.md)). Proven approaches: a
mature Tkinter desktop and a pywebview-over-static-frontend viewer.

## Approach (default)

1. Prefer a **shared frontend**:
   - Web-tech UI -> wrap with **pywebview** (WebView2 on Windows,
     WebKitGTK on Linux, WebKit on macOS) - one HTML/JS frontend serves
     browser, Docker, and desktop (Markview pattern).
   - Rich native Python desktop -> toolkit chosen **per app** and
     documented in its README. Tkinter/ttk + sv-ttk worked at large scale
     but is being moved away from there; PySide6 is the current
     experimental candidate for dense apps. Nothing is house-mandated.
2. Desktop shells add only platform bridges (open dialog, live reload,
   window state) behind a small JS bridge API - business logic stays in
   the core.
3. Portable binaries via **PyInstaller** per-app spec files
   (`markview.spec`, `packaging/<app>/<app>.spec`).

## Packaging command (default)

Every desktop app exposes **one canonical package command** (for example
`tools/package.py` or `build.ps1`) wrapping `pyinstaller --noconfirm
<app>.spec`. Build recipes live in tracked spec files - nobody
improvises builder flags, humans and agents included.

## Release machinery (default once binaries ship publicly)

Apps distributed beyond the dev desktop upgrade to the full release
pattern: one canonical packager script (`tools/build/package.py`)
that reads the version from code (single source), stages executables
under `out/<app>/stage/portable/`, emits versioned artifacts
(`App_v0.15.exe` + `.zip` / `.tar.gz`), and supports cross-builds via
Docker (`--win` / `--linux`). Before publishing: record artifact
inventory (contents, size, hash) and run the offline smoke test against
the produced binary (offline inventory + smoke runner). Ship
third-party license notices in bundles (`THIRD_PARTY_NOTICES.md`).

### Latest + versioned artifacts (pattern)

Keep **both** a stable "latest" binary and versioned historical
binaries so the last known-good build is always one path away and old
builds stay comparable. Lesson learned from a PyInstaller build script:

- Keep `dist\` intact - it holds the stable artifacts.
- Still delete `build\`, the build venv, and `src\app\static\dist`.
- Let PyInstaller overwrite `dist\App.exe` as the "latest" build.
- Copy it to a versioned name, e.g.
  `dist\App-1.0.0-20260830-1231.exe`
  (`App-<version>-<YYYYMMDD>-<HHMM>.exe`).

That yields a stable latest EXE plus versioned historical EXEs for
rollback and side-by-side comparison. This is a `(pattern)`, not a
mandate - it suits apps where a fixed `latest` filename is convenient
(e.g. an always-copied shortcut target). For pure release distributions
the versioned artifacts alone are enough.

macOS is treated as preview tier unless explicitly supported - say so in
the README instead of silently shipping broken builds.

Cross-platform constraints that apply here: see
[`10-cross-platform.md`](10-cross-platform.md). Release automation: see
[`11-releases.md`](11-releases.md).
