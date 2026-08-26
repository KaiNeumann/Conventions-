---
title: Wiki Conventions
type: reference
tags: [conventions, wiki]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Wiki Conventions

How we build and maintain knowledge bases (wikis) - for humans and agents.

These conventions apply to any vault we choose to run this way. Sections
are tiered per [`../README.md`](../README.md): **(rule)** binds,
**(default)** applies to new vaults unless noted, **(pattern)** is
reference material.

This area is reference documentation - verbose where it aids
understanding. Terse agent-loading distillations are derived artifacts,
extracted from here (see [`../README.md`](../README.md), "Purpose").

## Reading order

1. [`01-frontmatter.md`](01-frontmatter.md) - metadata schema for every note
2. [`02-notes-and-structure.md`](02-notes-and-structure.md) - atomic notes, naming, folders, links
3. [`03-obsidian-setup.md`](03-obsidian-setup.md) - Obsidian as the concrete tool
4. [`04-versioning-and-history.md`](04-versioning-and-history.md) - git versioning, documenting changes
5. [`05-human-agent-collaboration.md`](05-human-agent-collaboration.md) - who does what, safety rules
6. [`06-dynamic-views.md`](06-dynamic-views.md) - queries over curation (Dataview/Bases)
7. [`07-markdown-flavor.md`](07-markdown-flavor.md) - the house Markdown dialect and its extensions

## Core principles

- **Atomic** *(rule)* - one note, one topic. Split when a note answers two questions.
- **Linked** *(rule)* - no duplication; link to the single source of truth.
- **Frontmatter-driven** *(default)* - structure comes from metadata, so dynamic views assemble pages automatically.
- **Up to date beats complete** *(rule)* - update or flag, never leave silently wrong content.
- **Git-versioned** *(default)* - the vault is a repo; history is the audit trail.
