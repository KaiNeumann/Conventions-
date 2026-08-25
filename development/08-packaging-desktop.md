---
title: Packaging — Native Desktop Apps
type: reference
tags: [conventions, development, packaging]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Packaging — Native Desktop Apps

For when a desktop app makes sense. One part of the "one core, many
shells" model — the same core also ships as web app
([`07-packaging-web.md`](07-packaging-web.md)) and usually a headless CLI
(see [`05-languages.md`](05-languages.md)). Proven by RAT (mature
Tkinter desktop) and Markview (pywebview over a static frontend).

## Approach (default)

1. Prefer a **shared frontend**:
   - Web-tech UI → wrap with **pywebview** (WebView2 on Windows,
     WebKitGTK on Linux, WebKit on macOS) — one HTML/JS frontend serves
     browser, Docker, and desktop (Markview pattern).
   - Rich native Python desktop → **Tkinter/ttk** with sv-ttk theming
     (RAT's production-proven line); PySide6 exists only as an
     experimental packaged target, not production-proven.
2. Desktop shells add only platform bridges (open dialog, live reload,
   window state) behind a small JS bridge API — business logic stays in
   the core.
3. Portable binaries via **PyInstaller** per-app spec files
   (`markview.spec`, `packaging/<app>/<app>.spec`).

## Packaging command (default)

Every desktop app exposes **one canonical package command** (for example
`tools/package.py` or `build.ps1`) wrapping `pyinstaller --noconfirm
<app>.spec`. Build recipes live in tracked spec files — nobody
improvises builder flags, humans and agents included.

## Release machinery (default once binaries ship publicly)

Apps distributed beyond the dev desktop upgrade to the full release
pattern (RAT): one canonical packager script (`tools/build/package.py`)
that reads the version from code (single source), stages executables
under `out/<app>/stage/portable/`, emits versioned artifacts
(`App_v0.15.exe` + `.zip` / `.tar.gz`), and supports cross-builds via
Docker (`--win` / `--linux`). Before publishing: record artifact
inventory (contents, size, hash) and run the offline smoke test against
the produced binary (RAT qt_inventory/qt_smoke pattern). Ship
third-party license notices in bundles (`THIRD_PARTY_NOTICES.md`).

macOS is treated as preview tier unless explicitly supported — say so in
the README instead of silently shipping broken builds.

Cross-platform constraints that apply here: see
[`09-cross-platform.md`](09-cross-platform.md). Release automation: see
[`10-ci.md`](10-ci.md).
