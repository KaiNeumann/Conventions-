---
title: Human-Agent Collaboration
type: reference
tags: [conventions, wiki, agents]
status: accepted
created: 2026-08-23
updated: 2026-09-07
---

# Human-Agent Collaboration

Humans and agents edit the same vault. Applies wherever these wiki
conventions are in force.

## Access tiers (rule)

Tiers apply at **area level within one vault** - never one vault per
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
| `human-primary` | Humans are the authors; agents may prepare changes - committed locally, **never pushed**, every touched note marked `reviewed: false` for human review and push | none until reviewed |
| `human-only` | Read-only for agents: no edits, no staging, no exceptions without explicit instruction | none |

The secret prohibition applies in **all** tiers. Personal-data handling depends
on the publication boundary below; write tiers do not grant read access or
permission to disclose private information.

## Publication boundary (rule)

Clarification accepted 2026-09-07: private knowledge vaults may contain authorized
personal information needed for their purpose, including names, preferences,
contacts and personal history. The owner defines the audience and access policy.
Agents may use that information only within the granted scope. Indexes, snippets,
exports, backups and provider requests inherit the same confidentiality boundary.

Public repositories, reusable templates and publishable documentation use
placeholders rather than real personal or account details. Publishing or sending
private content to an external service requires authorization; a private vault
does not grant blanket permission to disclose it.

Passwords, API tokens, private keys, recovery codes and session credentials never
belong in ordinary notes, even private ones. Keep them in the approved secret
store. Refer to credential names or access procedures without copying values.
This distinction allows useful personal knowledge without turning the wiki into
a credential store or exposing it through public examples.

## Division of labor (default)

| Task | Human | Agent |
|---|---|---|
| Decide what the wiki contains, accept conventions | yes | |
| Write/edit notes, stubs, indexes | yes | yes |
| Restructure folders, mass renames | | yes proposes -> human approves (except `agent-managed`) |
| Accept/reject deprecations and deletions | yes | propose |
| Resolve merge conflicts | yes | prepare, never decide |
| Schema changes (frontmatter keys, types) | yes | propose via conventions change |

## Agent rules (rule)

1. **Read before write.** Read the vault `README.md` (including its tier
   map) and the target note before editing. Never invent structure that
   is already there.
2. **Preserve frontmatter.** Keep existing keys, bump `updated`.
3. **Fix links** after renames/splits, in the same change.
4. **No silent deletions.** Removing content requires explicit
   instruction. Otherwise: mark `status: deprecated` with a reason, or ask.
5. **No secrets in notes.** Authorized personal information belongs only in
   appropriately restricted private vaults. Public examples use `<user>` and
   other placeholders. Follow the publication boundary above.
6. **Small reviewable changes.** One logical change per commit so the
   human reviews diffs, not essays.
7. **Flag staleness, don't guess.** If content looks wrong but can't be
   verified, add `> [!warning] Unverified - <date>` instead of rewriting
   from memory.
8. **Mark provenance.** Notes an agent created or substantially rewrote
   carry `source: automation` and `reviewed: false` in frontmatter until
   a human clears them (`reviewed: true` / key removed).

## Human habits (default)

1. Audit `agent-managed` areas via diffs after the fact; review and push
   `human-primary` proposals; keep `human-only` boundaries intact.
2. Keep the vault `README.md` current - tier map included; it is the
   agents' entry point.
3. Push back on over-structure: an agent that creates 20 empty stubs gets
   told to stop.
