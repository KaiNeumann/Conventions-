---
title: Dynamic Views
type: reference
tags: [conventions, wiki, views]
status: draft
created: 2026-08-23
updated: 2026-09-16
---

# Dynamic Views

## Principle (default)

Views are **queried, not curated**. Any list derivable from frontmatter
and links is a query, not a hand-maintained list - queries stay correct
as notes change. If you are hand-writing a list a query could produce,
write the query.

This applies when a vault actually runs views. A small reference repo
that is read top-to-bottom may never need a dashboard; introduce views
when curation lists or "what's new" questions appear, not before.

## Tools (default)

- **Editor-native property views** (e.g. Obsidian Bases) - table views
  over note properties. Preferred when it covers the need.
- **Dataview** (community plugin) - when native views are not enough
  (grouping, complex filters).
- A vault without community plugins uses the editor's native search and
  property views; note the choice in the vault `README.md`.

## Standard views (default)

When a vault runs views, its root `dashboard.md` offers at least:

1. **Recent changes** - notes sorted by `updated` desc (top 20)
2. **Drafts** - all `status: draft`, so drafts never rot silently
3. **By type** - one table per `type` value
4. **Orphans** - notes with no incoming links

Folder indexes (MOCs) may embed the same queries scoped to their folder.

## Query hygiene (default)

1. Queries live in the note where they are used.
2. A query longer than ~10 lines signals the frontmatter schema needs a
   new key, not a bigger query.
3. Views are read-only artifacts - they never replace linking between
   notes.
