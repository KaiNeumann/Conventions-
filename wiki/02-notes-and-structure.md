---
title: Notes and Structure
type: reference
tags: [conventions, wiki, structure]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Notes and Structure

## Atomicity (rule)

1. One note answers **one question**. If a note needs two unrelated
   top-level `#` sections, split it.
2. Splitting is cheap: create the new note, move content, leave a wiki
   link behind.

Long is fine when it stays one topic (a setup guide can be long); mixed
topics are not.

## Linking (rule)

1. Content exists exactly once — **link, don't duplicate.**
2. After renames or splits, incoming links are fixed in the same change.
3. When you notice a missing note while writing, create it as a stub
   (frontmatter + one sentence + `status: draft`) rather than losing the
   thought.

## Link style (default)

1. Notes stay readable without wiki software — plain Markdown renders on
   Forgejo/GitHub and in any editor. Default to standard Markdown links
   for cross-note links.
2. Wikilinks (`[[...]]`) are acceptable in Obsidian-only vaults; pick per
   vault and document the choice in its `README.md`.
3. External URLs and files outside the vault always use standard
   Markdown links.

## Naming (default)

1. File names lowercase `kebab-case.md` (`boot-safety-meta-rules.md`);
   ASCII-safe characters preferred.
2. Name notes as the question they answer or the thing they describe
   (`tor-routing.md`, `2026-homeserver-setup.md`) — never `notes.md`,
   `untitled.md`, `misc.md`.
3. Numbered prefixes (`01-`, `02-`, …) only for ordered material: reading
   paths, step-by-step setup series — never plain topical notes.
4. Renames are welcome; fix links in the same commit.

## Folders (default)

1. Group by **area**, max ~3 levels deep (`projects/2026-homeserver/`,
   `howto/linux/`).
2. Every folder with more than ~7 notes gets a `README.md` index listing
   its notes with one-line descriptions.
3. Standalone notes stay as plain `.md` files beside their siblings.
4. A **page bundle counts as one unit** in folder arithmetic: one slot
   toward the index threshold, no extra depth level, and its internal
   assets are invisible to folder rules.

## Page bundles (rule)

An entry that carries **supporting files** (images, data, examples,
exports, …) MUST live as a **page bundle**: a subfolder named after the
entry containing the main `.md` plus everything that belongs to it.

```
projects/2026-homeserver/
├── README.md
└── boot-safety/
    ├── boot-safety.md
    ├── layout.png
    └── sample-crypttab.txt
```

1. Bundle name = entry name (`boot-safety/` ↔ `boot-safety.md`).
2. Reference supporting files with **relative links** — they survive
   moving the whole bundle anywhere in the vault.
3. Moving, renaming, or archiving an entry happens in **one filesystem
   operation**; nothing that belongs together can be left behind.
4. **No central attachment folders** — no `attachments/`, no `_shared/`,
   no per-area dumps. At hundreds-or-thousands scale those become
   unmanageable junk drawers. An asset used by several bundles gets
   duplicated into each one (storage is cheap, locality is valuable); if
   it's substantial enough to warrant single ownership, it becomes its
   own page bundle that others link to.
