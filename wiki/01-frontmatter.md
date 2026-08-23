---
title: Frontmatter
type: reference
tags: [conventions, wiki, metadata]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Frontmatter

Every note in a vault following these conventions starts with a YAML
frontmatter block (`---` delimited). Frontmatter is the machine-readable
layer that powers search, linking, and dynamic views.

The **key set below is the default schema** — a vault MAY extend or trim
it, but must document its schema in the vault `README.md`. The handling
rules (valid YAML, preserve keys, no secrets) are rules.

## Schema (default)

```yaml
---
title: Payment document extraction
type: note          # note | meeting | decision | howto | reference | person | project
tags: [pdf, extraction]
created: 2026-08-23
updated: 2026-08-23
---
```

| Key | Rule |
|---|---|
| `title` | Human-readable title. SHOULD match the first `#` heading. |
| `type` | One fixed value from the list above. Drives views and templates. |
| `tags` | List, lowercase, hyphen-separated (`payment-docs`, not `Payment Docs`). No free-form duplicates of `type`. |
| `created` | Date the note was created, ISO 8601 (`YYYY-MM-DD`). Set once, never edit. |
| `updated` | Date of last substantive change. Bump on content edits. |

Optional keys — add only when a view or workflow consumes them:

- `status: draft | accepted | deprecated` — for decisions and specs
- `source: <url or path>` — where external content came from
- `project: <name>` — link to a project note
- `aliases: [...]` — alternative names for linking

## Handling (rule)

1. Frontmatter **MUST** be valid YAML. Beware YAML quoting gotchas: in
   single-quoted strings `\` is literal (no escapes) — see RAT `AGENTS.md`
   for the failure table. Prefer double quotes when values contain `:`,
   `#`, or `\`.
2. **NEVER** store secrets, personal data, or long prose in frontmatter.
   It is metadata, not content.
3. Agents **MUST** preserve existing frontmatter keys when editing a note
   and bump `updated` on substantive changes.
4. Schema changes (new key, new `type` value) are changes to this
   conventions file first, then to the notes.

This conventions repository itself follows this schema — it is the
reference implementation, not a special case.
