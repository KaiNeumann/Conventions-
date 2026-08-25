---
title: Human–Agent Collaboration
type: reference
tags: [conventions, wiki, agents]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Human–Agent Collaboration

Humans and agents edit the same vault. Applies wherever these wiki
conventions are in force.

## Access tiers (rule)

Tiers apply at **area level within one vault** — never one vault per
tier; a vault remains a single self-contained workspace. Each vault's
`README.md` carries a tier map assigning every top-level area (folder)
its tier; undeclared areas default to **human-primary**. Example, all
inside the same vault:

```
Kai/     -> human-only      # personal notes agents may read, never write
Family/  -> human-primary   # agents prepare, humans review & push
Howto/   -> agent-managed   # agents write and push autonomously
```

| Tier | Meaning | Agent push rights |
|---|---|---|
| `agent-managed` | Agents create, edit, and push autonomously; humans audit diffs after the fact | direct |
| `human-primary` | Humans are the authors; agents may prepare changes — committed locally, **never pushed**, every touched note marked `reviewed: false` for human review and push | none until reviewed |
| `human-only` | Read-only for agents: no edits, no staging, no exceptions without explicit instruction | none |

Secrets/personal-data prohibitions apply in **all** tiers.

## Division of labor (default)

| Task | Human | Agent |
|---|---|---|
| Decide what the wiki contains, accept conventions | ✅ | |
| Write/edit notes, stubs, indexes | ✅ | ✅ |
| Restructure folders, mass renames | | ✅ proposes → human approves (except `agent-managed`) |
| Accept/reject deprecations and deletions | ✅ | propose |
| Resolve merge conflicts | ✅ | prepare, never decide |
| Schema changes (frontmatter keys, types) | ✅ | propose via conventions change |

## Agent rules (rule)

1. **Read before write.** Read the vault `README.md` (including its tier
   map) and the target note before editing. Never invent structure that
   is already there.
2. **Preserve frontmatter.** Keep existing keys, bump `updated`.
3. **Fix links** after renames/splits, in the same change.
4. **No silent deletions.** Removing content requires explicit
   instruction. Otherwise: mark `status: deprecated` with a reason, or ask.
5. **No secrets, no personal data** in notes — same bar as code repos
   (no usernames, no account data; use `<user>` placeholders).
6. **Small reviewable changes.** One logical change per commit so the
   human reviews diffs, not essays.
7. **Flag staleness, don't guess.** If content looks wrong but can't be
   verified, add `> [!warning] Unverified — <date>` instead of rewriting
   from memory.
8. **Mark provenance.** Notes an agent created or substantially rewrote
   carry `source: automation` and `reviewed: false` in frontmatter until
   a human clears them (`reviewed: true` / key removed).

## Human habits (default)

1. Audit `agent-managed` areas via diffs after the fact; review and push
   `human-primary` proposals; keep `human-only` boundaries intact.
2. Keep the vault `README.md` current — tier map included; it is the
   agents' entry point.
3. Push back on over-structure: an agent that creates 20 empty stubs gets
   told to stop.
