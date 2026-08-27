---
title: Documentation Standards
type: reference
tags: [conventions, development, documentation]
status: accepted
created: 2026-08-23
updated: 2026-08-26
---

# Documentation Standards

Docs are part of done. Three layers: README (humans, first contact),
AGENTS.md (agents, safety + context), docs/ (depth).

## README.md (every repo) (default)

The README is the **storefront**: it introduces the project to
outsiders and answers *what / why / how-to-try* within the first
screenful. Development history, architecture deep-dives, and annotated
project trees belong in `docs/` - linked, not inlined.

Structure (cognitive funnel: broadest first, narrowing for the
committed reader):

````markdown
# Name
One sentence: what it does, for whom, and the one differentiator.

![screenshot or demo](docs/media/demo.png)

## Features
Scannable bullet list of key capabilities — differentiators first,
concrete claims, no marketing fluff.

## Why
Short motivation from the reader's perspective.

## Quick Start
≤5 copy-paste commands; visible result in under a minute.

## Usage
Examples of the main flows (commands, screenshots).

## Configuration
Table: setting | purpose | default — user-facing settings only.

## Limitations & FAQ
Honest limits up front.

## Documentation
Links into docs/: architecture, operations, decision records,
development guide.

## Contributing & Development
Build/test/lint commands in brief; full details in docs/.

## License
SPDX name and owner.
````

Optional sections where they earn their place: badges, Troubleshooting,
Security Notes, an Architecture diagram (only when the architecture is
the pitch).

Rules:

- *(rule)* Quickstart commands are tested in a clean environment;
  claims match reality ("zero dependencies", "offline" must be true).
- *(rule)* The first screenful answers what/why/how-to-try; show the
  app early (screenshot or demo).
- *(default)* As short as possible - details migrate into `docs/`
  aggressively; link instead of inline.
- *(default)* Written for an outside reader, not for the authors'
  memory.
- *(default)* Explicit non-goals: include a list of explicit non-goals (such as "no cloud model dependencies", "single-user only") to establish a strict scope ceiling.
## AGENTS.md (rule for agent-worked repos)

Every repo an agent regularly works in **MUST** have an `AGENTS.md` -
short, practical rules for automated changes. Required
sections:

1. *(rule)* **Safety gates first** - non-negotiables up top (never
   access secret stores without explicit approval; network-restricted
   tools keep their routing rules). An agent must hit these in the first
   lines.
2. **Global rules** - environment (venv path, OS/shell assumptions),
   portability (no hardcoded paths, no env-var app config), testing
   policy (deterministic vs live-network), destructive-command ban.
3. **Architecture pointers** - what lives where, canonical imports,
   deprecated zones ("frozen, migration source only").
4. **Known gotchas** - hard-won traps with wrong/right examples
   (YAML quoting table, line endings, encoding).
5. *(rule)* **Privacy rules** - no usernames/personal data in issues, logs,
   examples.

Keep it under ~200 lines; depth belongs in docs/.

## Inline comments (default)

1. Comment **why**, not what. The code says what; the comment says why
   this and not the obvious alternative.
2. Mark deliberate simplifications with their ceiling and upgrade path:

   ```python
   # ponytail: O(n^2) scan fine until >10k items; switch to index when profiled
   ```

3. No commented-out code in commits - delete it; git remembers.
4. Public APIs get docstrings; internals only when non-obvious.

## Deeper docs (`docs/`) (default)

1. Numbered series for journeys (`2026-setup/00-architecture/...`,
   `01-install`, ...) with a `README.md` reading-order index.
2. Decision records: house default is a **Key Decisions** list (one line
   each, in `README.md` or `AGENTS.md`). A decision needing more than a
   paragraph of context escalates to a numbered doc under `docs/`
   (context / decision / consequences), referenced from that list.
3. Topical troubleshooting/handbooks live under `docs/<area>/`.
4. *(rule)* **No root-level clutter:** everything except `README.md` and
   `AGENTS.md` lives under `docs/` from day one - including status
   snapshots and troubleshooting guides (`docs/status/...`,
   `docs/<area>/troubleshooting.md`). Roots stay scannable.

## Prose style *(rule)*

All texts follow anti-AI-tell writing rules (derived from Wikipedia's
"Signs of AI writing"; see the MIT-licensed humanizer skills such as
blader/humanizer and anti-ai-writing):

1. **No em/en dashes.** Use a period, comma, colon, parentheses, or a
   plain hyphen instead.
2. **No AI vocabulary:** delve, leverage (verb), robust, seamless,
   comprehensive, notably, pivotal, foster, facilitate, unlock,
   streamline, crucial, tapestry, testament.
3. **No fake significance** ("stands as a testament", "pivotal moment")
   and no participle padding (", highlighting ...").
4. **No negative parallelism** ("not just X, it's Y") and no forced
   rule-of-three lists.
5. **Plain copulas:** is/are, not "serves as / functions as / stands as".
6. Cut hedging filler ("it is worth noting") and formulaic connectors
   (moreover, furthermore, additionally); no hollow conclusions.
7. Specifics beat vague claims; vary sentence rhythm.

Meta-rule: one pattern alone proves nothing, clusters count. And never
change facts while restyling.

*(default)* Repository Markdown is **UTF-8 without BOM**. Umlauts,
accented Latin, ligatures (æ, œ, ß), and common scientific symbols are
fine in prose. Banned everywhere: BOM, non-breaking/zero-width spaces.
Box-drawing trees and arrows stay inside fenced code blocks (monospace
rendering, not encoding).

*(rule)* CI rejects invalid UTF-8 and BOMs (one-line `iconv -f utf-8
-t utf-8 <file>` round-trip check).

## Up-to-dateness *(rule)*

Any change that invalidates documentation fixes the documentation in the
same commit. Docs that lie are worse than missing docs.
