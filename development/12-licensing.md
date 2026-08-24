---
title: Licensing
type: reference
tags: [conventions, development, licensing]
status: accepted
created: 2026-08-24
updated: 2026-08-24
---

# Licensing

Every license answers one question: **what do you want to prevent?**
Pick by repo category from the table below instead of re-litigating per
project.

## Decision table (rule)

| Repo type | License | Why |
|---|---|---|
| Private infra & personal tools | **All rights reserved** (explicitly declared) | Security topology and personal context; publishing later becomes a conscious act with a fresh license choice |
| Libraries, skills, templates others **build upon** | **MIT** | Permissive maximizes reuse; copyleft obligations repel exactly the casual embedding these exist for |
| Standalone apps/tools a community **uses or forks** | **GPL-3.0** | End users are unaffected; re-developers must keep forks open — commons protection without user friction |
| Network-served apps others could **host** | **AGPL-3.0** | Closes the SaaS loophole. Also the default for professional-service/portfolio apps: sole copyright holder keeps service freedom plus the dual-licensing option (permissive would burn it forever) |
| Prose: docs, wiki, conventions, design docs | **CC-BY-SA-4.0** | Code licenses fit prose badly; attribution + share-alike |

Additional rules:

1. Every repository **MUST** declare its license explicitly — SPDX
   identifier in `pyproject.toml` / `package.json`, `LICENSE` file at
   root once public. *Undeclared = undecided*, and undeclared means
   all-rights-reserved whether you meant it or not.
2. Repos whose prose differs from their code carry a one-line footer:
   `License: code GPL-3.0 · docs CC-BY-SA-4.0`.
3. Shipped binaries bundle third-party material: include
   `THIRD_PARTY_NOTICES.md` (RAT pattern).
4. Relicensing a public repository is a significant event: human
   sign-off required, announced in the repo's README or changelog.
5. German/EU moral rights (Urheberrecht) are non-waivable but fully
   compatible with every license named here — no extra clauses needed.

## Mechanics

```toml
# pyproject.toml
license = {text = "GPL-3.0"}        # SPDX identifiers only
```

```json
// package.json
"license": "AGPL-3.0"
```

No per-file license headers; the LICENSE file plus declarations suffice.

## Target state for existing repos

Mapping decided 2026-08-24 — migrations happen as ordinary tasks, not
automatically:

| Repo(s) | Today | Target |
|---|---|---|
| homeserver, conventions, money, Finanzen, Blutwerte, … private set | undeclared | declare all-rights-reserved |
| RAT (public on Codeberg) | Proprietary | GPL-3.0 — users gain freedom, forks stay open, exposure unchanged (source was already public) |
| markdownviewer, organizer, rss-creator (community standalone tools) | undeclared | GPL-3.0 |
| GoldsteinCMS | AGPL-3.0 | already conforms |
| agent-skills, OpenClaw-Skills, reusable templates | undeclared | MIT |
| All docs/wiki prose inside mixed repos | n/a | CC-BY-SA-4.0 footnote |
| Food-and-Nutrition | MIT | keep (declared licenses stand unless owner opts to migrate) |
