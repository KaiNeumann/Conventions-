---
title: Obsidian Setup
type: reference
tags: [conventions, wiki, obsidian]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Obsidian Setup

Obsidian is the concrete editor for wikis. The vault is a plain folder of
Markdown files — git and agents work on the files, Obsidian is a view on
top.

## Vault in git (default)

A vault following these conventions is a git repository; the vault root is
the repo root.

1. Commit `.obsidian/` selectively (snippet below) — this part is rule:
   machine-local state never enters git.

```gitignore
# Obsidian: ignore machine-local state, keep shared config
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
```

2. Use the **Obsidian Git** community plugin *or* plain git in a terminal —
   pick one per vault and say so in the vault `README.md`.

## Plugins (default)

1. Core plugins only where needed: backlinks, outgoing links, templates,
   outline, search.
2. Community plugins stay minimal and justified:
   - *Dataview* or built-in *Bases* — dynamic views (see
     [`06-dynamic-views.md`](06-dynamic-views.md))
   - *Obsidian Git* — versioning
3. Every vault documents its enabled plugins in its `README.md`, so agents
   know what syntax is safe to emit.

## Templates (default)

1. One template per `type` from the frontmatter schema, stored in
   `templates/`.
2. Templates contain the full frontmatter block with placeholder values.
3. New notes are created from templates where practical; agents
   reproduce the frontmatter schema exactly regardless.

## Portability (rule)

1. No CDN links, no external services required to read notes — the vault
   renders offline (same rule as Markview: vendor or go without).
2. Images and PDFs are stored inside the vault (`attachments/`), not
   hot-linked.
