---
title: Packaging - Native Desktop Apps
type: reference
tags: [conventions, development, packaging]
status: accepted
created: 2026-08-23
updated: 2026-09-02
---

# Packaging - Native Desktop Apps

For when a desktop app makes sense. One part of the "one core, many
shells" model - the same core also ships as web app
([`08-packaging-web.md`](08-packaging-web.md)) and usually a headless CLI
(see [`05-languages.md`](05-languages.md)).

## Desktop or not? *(default)*

Not every repo gets an exe. Three sanctioned shapes:

1. **Desktop app** - a local single-user GUI. Ships as portable exe via
   the machinery below.
2. **Service** - UI is a convenience, app runs headless most of the time.
   Docker-first ([`08-packaging-web.md`](08-packaging-web.md)); an exe,
   if built at all, is a console binary that starts the server and opens
   the browser. No desktop window investment.
3. **No desktop shell** - multi-service platforms and pure APIs. Docker /
   compose only.

Native widget toolkits (Tkinter, PySide) remain allowed when the app
depends on a heavy native stack (ML models, deep OS integration) where a
web frontend adds nothing - say so in the README and still package with
the same canonical harness.

## Approach (default)

1. Prefer a **shared frontend**: one HTML/JS UI serves browser, Docker,
   and desktop. Web-tech UI -> wrap with **pywebview** (WebView2 on
   Windows, WebKitGTK on Linux, WebKit on macOS).
2. Desktop shells add only platform bridges (open/save dialog, window
   state) behind a small JS bridge API - business logic stays in the
   core.
3. The desktop entry point is `packaging/desktop_main.py`, and
   everywhere it does the same five things - pick a free port, start the
   server in a thread, `webview.create_window(url)`, on window close shut
   the server down, fall back to the system browser when pywebview is
   unavailable. Write no fourth variant of this.
4. Portable binaries via **PyInstaller one-file** spec files in
   `packaging/<app>.spec`. Specs collect `webview` via
   `collect_all('webview')` - never bundle `WebView2Loader.dll` by hand,
   current pywebview resolves it itself. `upx=False` (AV false
   positives), `console=False` on windowed apps.
5. **Portable sidecar data**: a shipped exe stores its data (db, media,
   logs) next to the exe, never inside it - see
   [`10-cross-platform.md`](10-cross-platform.md) and
   [`14-settings.md`](14-settings.md).

## Canonical build harness *(default)*

One command builds everything the repo supports:

```powershell
python tools/build.py
```

`tools/build.py` is copied from the reference implementation
([`templates/tools/build.py`](templates/tools/build.py)) and is the only
build entry point. It is opinionated: stages are auto-detected from repo
layout, not configured.

1. **clean** - remove `build/`, `dist/`, stale bundled frontend output.
2. **frontend** - if `frontend/package.json` exists: `npm ci`, `npm test`,
   `npm run build`.
3. **deps** - reuse the current environment when PyInstaller is
   importable, otherwise create a throwaway `build/venv`.
4. **exe** - run every `packaging/*.spec`.
5. **stamp** - `dist/<App>.exe` is the stable "latest"; add a versioned
   copy `dist/<App>-<version>-<YYYYmmdd-HHMM>.exe`. Version is imported
   from the package (`__version__`) - never parsed from text output.
6. **self-test** - each produced exe must accept `--self-test` and exit
   nonzero on failure; build fails when it does. Frozen apps without a
   self-test are not releasable.
7. **inventory** - write `dist/INVENTORY.json` (name, size, sha256, git
   rev, timestamp) for every artifact.
8. **docker** - only with `--docker` (CI releases per
   [`08-packaging-web.md`](08-packaging-web.md)): build the runtime
   image, tag `:<version>` and `:latest`.

Shell wrappers (`build.ps1`) are optional two-line shims calling
`tools/build.py` - never the home of build logic.

Cross-builds: produce a Linux exe by running the same `tools/build.py`
inside a Linux build container (Python slim + build-essential +
WebKitGTK dev headers) with the repo mounted. Windows exes are built on
Windows; the planned Wine runner
([`12-task-automation.md`](12-task-automation.md)) flips that later, not
the repos.

## Release extras (default once binaries ship publicly)

- `THIRD_PARTY_NOTICES.md` ships in bundles
  ([`15-licensing.md`](15-licensing.md)).
- Release automation and provenance follow
  [`11-releases.md`](11-releases.md); record the git rev of every
  shipped artifact (the inventory does this).
- macOS is preview tier unless a project explicitly commits - say so in
  the README instead of silently shipping broken builds.
