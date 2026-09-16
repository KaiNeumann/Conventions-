---
title: Editor Setup
type: reference
tags: [conventions, wiki, editor]
status: draft
created: 2026-08-23
updated: 2026-09-16
---

# Editor Setup

The editor is a view on top of a plain Markdown folder. Git and agents
work on the files; the editor renders and edits them. Any editor that
stores notes as plain Markdown and renders the house dialect
([`07-markdown-flavor.md`](07-markdown-flavor.md)) qualifies. A vault
documents its chosen editor in its `README.md`, so agents know what
syntax and features are safe to use.

## Vault in git (default)

A vault following these conventions is a git repository; the vault root is
the repo root.

1. Commit editor configuration selectively - this part is rule:
   machine-local state never enters git. The exact ignored paths depend
   on the editor; for an Obsidian-style editor the snippet below applies.

```gitignore
# Editor: ignore machine-local state, keep shared config
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
```

2. Version through the editor's git integration or plain git in a
   terminal - pick one per vault and say so in the vault `README.md`.

## Plugins (default)

1. Core features only where needed: backlinks, outgoing links, templates,
   outline, search.
2. Extensions stay minimal and justified:
   - a query/view plugin (e.g. Dataview) or editor-native property views
     for dynamic views (see [`06-dynamic-views.md`](06-dynamic-views.md))
   - git integration for versioning
3. Every vault documents its enabled plugins in its `README.md`, so agents
   know what syntax is safe to emit.

## Templates (default)

1. One template per `type` from the frontmatter schema, stored in
   `templates/`.
2. Templates contain the full frontmatter block with placeholder values.
3. New notes are created from templates where practical; agents
   reproduce the frontmatter schema exactly regardless.

## Portability (rule)

1. No CDN links, no external services required to read notes - the vault
   renders offline (same rule as Markview: vendor or go without).
2. Supporting files are stored **inside the vault as page bundles**
   ([`02-notes-and-structure.md`](02-notes-and-structure.md)) - never
   hot-linked, never scattered into a central attachments dump.
