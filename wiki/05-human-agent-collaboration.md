---
title: Human–Agent Collaboration
type: reference
tags: [conventions, wiki, agents]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Human–Agent Collaboration

Humans and agents edit the same vault. Applies wherever these wiki
conventions are in force.

## Division of labor (default)

| Task | Human | Agent |
|---|---|---|
| Decide what the wiki contains, accept conventions | ✅ | |
| Write/edit notes, stubs, indexes | ✅ | ✅ |
| Restructure folders, mass renames | | ✅ (propose → human approves) |
| Accept/reject deprecations and deletions | ✅ | propose |
| Resolve merge conflicts | ✅ | prepare, never decide |
| Schema changes (frontmatter keys, types) | ✅ | propose via conventions change |

## Agent rules (rule)

1. **Read before write.** Read the vault `README.md`/index and the target
   note before editing. Never invent structure that is already there.
2. **Preserve frontmatter.** Keep existing keys, bump `updated`.
3. **Fix links** after renames/splits, in the same change.
4. **No silent deletions.** Removing content requires explicit
   instruction. Otherwise: mark `status: deprecated` with a reason, or ask.
5. **No secrets, no personal data** in notes — same bar as code repos
   (RAT rule: no usernames, no account data; use `<user>` placeholders).
6. **Small reviewable changes.** One logical change per commit so the
   human reviews diffs, not essays.
7. **Flag staleness, don't guess.** If content looks wrong but can't be
   verified, add `> [!warning] Unverified — <date>` instead of rewriting
   from memory.

## Human habits (default)

1. Review agent commits via git diff before push.
2. Keep the vault `README.md` current — it is the agents' entry point.
3. Push back on over-structure: an agent that creates 20 empty stubs gets
   told to stop.
