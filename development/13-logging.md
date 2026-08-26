---
title: Logging
type: reference
tags: [conventions, development, logging]
status: accepted
created: 2026-08-24
updated: 2026-08-24
---

# Logging

Logs answer "what happened, when, to what?" - for humans scanning a
file and for agents/scripts filtering it. Both readers get served by the
same rules.

## Location *(default)*

1. All runtime logs live under **`logs/`** in the app's data or profile
   directory - never scattered next to code, never in temp dirs.
   Containerized deployments log to **stdout/stderr** instead
   (daemon-collected, size-bounded rotation) - see the operations
   conventions; the format rules below still apply to those lines.
2. `logs/` is always gitignored and dockerignored (standard-file
   templates already do).
3. File naming *(default)*: `logs/<app>.log`, plain append mode;
   size-based rotation only for long-running services.
4. Logs are **disposable**: they are diagnostics, never a data store.
   Anything that must survive belongs in real state (database/settings),
   not in a log line.

## Entry format *(rule)*

Every entry is **timestamped** and carries **identifiers that make it
filterable**:

```
2026-08-24T21:15:04+02:00 INFO  transfer  task=42 upload finished file=report.pdf size=2.3MiB duration=12s
2026-08-24T21:15:07+02:00 WARN  scheduler hoster=rapidshare rate-limit hit backoff=300s
```

1. **Timestamp**: ISO 8601 with explicit UTC offset, at line start.
2. **Level**: `DEBUG` / `INFO` / `WARN` / `ERROR` from a fixed
   vocabulary.
3. **Identifiers**: each entry names what it concerns - app/component
   plus the relevant entity id (`task=42`, `hoster=rapidshare`) - used
   *consistently across the whole stream*. The exact shape is free per
   app; three properties are required:
   - greppable: one unit's full story is extractable by filtering on
     its identifier,
   - not overly verbose, no decorative formatting,
   - structured enough for machines (`key=value` pairs or JSON fields).
4. One line per event when possible; services preferring JSON emit one
   object per line with the same fields.

## Noise control *(rule)*

1. `DEBUG` is off by default and toggled via settings - never needed to
   understand normal operation.
2. Repeating messages are throttled or deduplicated (state the repeat
   count instead of re-printing).
3. No secrets, tokens, or personal data in any level - placeholders
   follow the privacy rules ([`01-git.md`](01-git.md)).

## GUI & agent behavior *(default)*

1. GUIs surface state in the interface (statusbar/toast) and write the
   detail to the log - the log is the deep layer, not the primary UX.
2. Agents debugging read **log tails** (`--tail` / last N lines) and
   grep by identifier - never cat whole files into context.
3. Long-running apps bound their logs (size-based rotation); old logs
   may be deleted without ceremony.
