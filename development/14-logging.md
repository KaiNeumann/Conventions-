---
title: Logging
type: reference
tags: [conventions, development, logging]
status: draft
created: 2026-08-24
updated: 2026-08-24
---

# Logging

Logs answer "what happened, when, to what?" — for humans scanning a
file and for agents/scripts filtering it. Both readers get served by the
same rules.

## Location *(default)*

1. All runtime logs live under **`logs/`** in the app's data or profile
   directory — never scattered next to code, never in temp dirs.
2. `logs/` is always gitignored and dockerignored (standard-file
   templates already do).
3. Logs are **disposable**: they are diagnostics, never a data store.
   Anything that must survive belongs in real state (database/settings),
   not in a log line.

## Entry format *(rule)*

Every entry is **timestamped and filterable**:

```
2026-08-24T21:15:04+02:00 INFO  [transfer][task-42] upload finished: report.pdf (2.3 MiB, 12s)
2026-08-24T21:15:07+02:00 WARN  [scheduler] hoster rate-limit hit, backing off 300s
```

1. **Timestamps**: ISO 8601 with explicit UTC offset, at line start.
2. **Level**: `DEBUG` / `INFO` / `WARN` / `ERROR` from a fixed
   vocabulary.
3. **Filterable identifiers**: every entry tied to an entity carries
   stable bracketed tags up front — component plus the relevant id
   (`[transfer][task-42]`, `[scraper][site-x]`). Anyone must be able to
   extract one unit's full story with a plain `grep '[task-42]'`.
4. One line per event when possible; structured `key=value` pairs for
   machine parsing. Services that emit JSON log one object per line.

## Noise control *(rule)*

1. `DEBUG` is off by default and toggled via settings — never needed to
   understand normal operation.
2. Repeating messages are throttled or deduplicated (state the repeat
   count instead of re-printing).
3. No secrets, tokens, or personal data in any level — placeholders
   follow the privacy rules ([`01-git.md`](01-git.md)).

## GUI & agent behavior *(default)*

1. GUIs surface state in the interface (statusbar/toast) and write the
   detail to the log — the log is the deep layer, not the primary UX.
2. Agents debugging read **log tails** (`--tail` / last N lines) and
   grep by identifier — never cat whole files into context.
3. Long-running apps bound their logs (size-based rotation); old logs
   may be deleted without ceremony.
