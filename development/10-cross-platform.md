---
title: Cross-Platform Rules
type: reference
tags: [conventions, development, portability]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Cross-Platform Rules

Bind across all delivery modes (web, desktop, CLI — see
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
