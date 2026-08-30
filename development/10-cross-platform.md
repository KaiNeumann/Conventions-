---
title: Cross-Platform Rules
type: reference
tags: [conventions, development, portability]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Cross-Platform Rules

Bind across all delivery modes (web, desktop, CLI - see
[`08-packaging-web.md`](08-packaging-web.md),
[`09-packaging-desktop.md`](09-packaging-desktop.md)) and complement the
language-level standards in [`05-languages.md`](05-languages.md).

1. *(rule)* No hardcoded absolute paths; `pathlib.Path` everywhere;
   defaults relative to app/profile dirs.
2. *(rule)* Explicit UTF-8 on all text IO; LF in repo, per-OS only where
   forced.
3. *(default)* Windows + PowerShell is a first-class target (that is
   where we work); test Linux paths via Docker.
4. *(default)* Config via persisted settings files (portable INI/YAML
   next to app or in profile dir); env-var config only inside
   containers/test harnesses.
5. *(default)* **Portable artifact**: a shipped desktop binary is
   self-contained - no runtime dependency beyond the OS itself
   (PyInstaller one-folder/one-file). It must run from any folder
   without an installer or prior setup. It is produced once per target
   OS, never reused across OSes.
6. *(default)* **Cross-compilation**: produce a target OS's binary from
   a different build host where practical. The planned route is
   Wine-based cross-builds on a Linux runner for Windows targets
   ([`12-task-automation.md`](12-task-automation.md)); before that
   lands, build locally on the native OS (Windows dev desktop for
   Windows EXEs). Python is not directly cross-compilable - the binary
   must be built on (or under Wine for) the target OS.
