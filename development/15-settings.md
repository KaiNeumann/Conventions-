---
title: Settings & Persistence
type: reference
tags: [conventions, development, settings]
status: accepted
created: 2026-08-24
updated: 2026-08-24
---

# Settings & Persistence

Apps persist configuration and user state in files that humans can read,
edit, back up, and copy between machines. This extends the persistence
principles in [`13-gui-design.md`](13-gui-design.md) and the no-env-var
boundary in [`09-cross-platform.md`](09-cross-platform.md).

## Location *(default)*

1. **Portable apps** (run from a folder/exe): sidecar file(s) **next to
   the executable** — a `<app>.json` sidecar. Copying
   the folder copies the app *with* its settings.
2. **Installed apps**: settings in the per-user profile directory
   (`%APPDATA%\<app>\`, `~/.config/<app>/`). Never write next to program
   files.
3. If the portable location is not writable (read-only medium), fall
   back to the profile dir automatically and say so once.
4. Multi-app repositories may share one `common` settings file beside
   per-app files.
5. Sidecar naming and format are free per app but **MUST be documented
   in the README** — agents and scripts locate settings through that
   documentation.

## Format *(default)*

1. Human-readable and hand-editable: JSON, YAML, or INI. Comments where
   the format allows them.
2. One file per app plus optional shared file; split by concern only
   when a file outgrows one screen.
3. Include a `version` key once the schema is non-trivial, so later
   migrations can be deterministic.

## Resilience *(rule)*

1. Missing file ⇒ start with built-in defaults; never require setup to
   reach a working state.
2. Corrupt or invalid values ⇒ fall back to the default for that key,
   **log a warning**, and keep the rest — never refuse to start over one
   bad key.
3. Unknown keys are preserved on rewrite (forward compatibility across
   versions).
4. After every write, the file must still parse — writes are atomic
   (temp file + rename).

## Sensitive values *(rule)*

1. Passwords, tokens, and similar credentials are **never stored
   plaintext** inside regular settings files.
2. **Portability-aware choice**:
   - Installed apps → prefer the OS credential store/keychain.
   - Portable sidecar apps → app-level encryption with a master password
     (encrypted blob + unlock prompt) — an OS store would
     break folder-copy portability.
3. Minimum fallback everywhere: a separate credential file with
   restrictive permissions, excluded from backups/exports.
4. Encryption keys are never derived from anything committed to the
   repo.

## One settings truth *(rule)*

GUI, CLI, and web UI read and write the **same** settings store through
one shared code path. No parallel config mechanisms per shell.

## Automation & agents *(default)*

1. Every settings file has a documented schema (README or spec file);
   agents validate after editing instead of assuming success.
2. Env-var overrides remain reserved for containers and test harnesses
   ([`09-cross-platform.md`](09-cross-platform.md)).
