---
title: Documentation Standards
type: reference
tags: [conventions, development, documentation]
status: accepted
created: 2026-08-23
updated: 2026-08-23
---

# Documentation Standards

Docs are part of done. Three layers: README (humans, first contact),
AGENTS.md (agents, safety + context), docs/ (depth).

## README.md (every repo) (default)

Structure (matches existing repos):

```markdown
# Name
One paragraph: what it is, for whom.

## Features            ← bullet list, concrete
## Quick Start         ← copy-paste-runnable (local AND docker)
## Configuration       ← table: setting | purpose | default
## Project Structure   ← annotated tree
## Architecture        ← diagram or flow description (when non-trivial)
## Development         ← install, test, lint commands
## Troubleshooting     ← known failure modes (when they exist)
## Security Notes      ← when security-relevant
## License
```

*(rule)* Quickstart commands are tested and claims match reality ("zero
dependencies", "offline" must be true).

## AGENTS.md (rule for agent-worked repos)

Every repo an agent regularly works in **MUST** have an `AGENTS.md` —
short, practical rules for automated changes (RAT style). Required
sections:

1. *(rule)* **Safety gates first** — non-negotiables up top (e.g. RAT's vault
   rule: never access secrets without explicit approval; ScraperCMS:
   Tor-only networking). An agent must hit these in the first lines.
2. **Global rules** — environment (venv path, OS/shell assumptions),
   portability (no hardcoded paths, no env-var app config), testing
   policy (deterministic vs live-network), destructive-command ban.
3. **Architecture pointers** — what lives where, canonical imports,
   deprecated zones ("frozen, migration source only").
4. **Known gotchas** — hard-won traps with wrong/right examples
   (YAML quoting table, line endings, encoding).
5. *(rule)* **Privacy rules** — no usernames/personal data in issues, logs,
   examples.

Keep it under ~200 lines; depth belongs in docs/.

## Inline comments (default)

1. Comment **why**, not what. The code says what; the comment says why
   this and not the obvious alternative.
2. Mark deliberate simplifications with their ceiling and upgrade path:

   ```python
   # ponytail: O(n²) scan fine until >10k items; switch to index when profiled
   ```

3. No commented-out code in commits — delete it; git remembers.
4. Public APIs get docstrings; internals only when non-obvious.

## Deeper docs (`docs/`) (default)

1. Numbered series for journeys (`2026-setup/00-architecture/…`,
   `01-install`, …) with a `README.md` reading-order index.
2. Decision records: house default is a **Key Decisions** list (one line
   each, in `README.md` or `AGENTS.md`). A decision needing more than a
   paragraph of context escalates to a numbered doc under `docs/`
   (context / decision / consequences), referenced from that list.
3. Topical troubleshooting/handbooks live under `docs/<area>/`.
4. *(rule)* **No root-level clutter:** everything except `README.md` and
   `AGENTS.md` lives under `docs/` from day one — including status
   snapshots and troubleshooting guides (`docs/status/…`,
   `docs/<area>/troubleshooting.md`). Roots stay scannable.

## Up-to-dateness rule (rule)

Any change that invalidates documentation fixes the documentation in the
same commit. Docs that lie are worse than missing docs.
