---
title: Markdown Flavor
type: reference
tags: [conventions, wiki, markdown]
status: accepted
created: 2026-08-24
updated: 2026-08-24
---

# Markdown Flavor

House dialect: CommonMark + GitHub-flavored Markdown **plus** the
extensions our toolchain renders natively (the Markview set). Write
within this dialect so every consumer - Obsidian, Markview,
Forgejo/GitHub - shows the note as intended.

## Supported extensions

| Feature | Syntax | Degrades to (plain/Forgejo renderers) |
|---|---|---|
| Tables | GFM pipes | renders fine |
| Task lists | `- [ ]` | renders fine |
| Strikethrough | `~~text~~` | renders fine |
| Alerts | `> [!NOTE]` / `[!WARNING]` ... | plain blockquote |
| Footnotes | `[^1]` | inline marker text |
| Emoji shortcodes | `:tada:` | literal text |
| Sub/superscript | `^sub^` / `^sup^` | literal carets |
| Highlight | `==text==` | literal equals signs |
| Math | `$...$` and `$$...$$` (KaTeX) | literal dollars |
| Diagrams | ` ```mermaid ` fences | fenced code block |
| Inline HTML | `<kbd>Ctrl</kbd>` - sparingly | sanitized (DOMPurify in Markview) |

Frontmatter stays YAML per [`01-frontmatter.md`](01-frontmatter.md).

## Rules

1. *(default)* Stay inside the dialect. An extension not listed above
   requires a change to this file first - and support in the rendering
   toolchain.
2. *(default)* Prefer constructs that degrade gracefully; the last
   column shows what plain renderers display instead.
3. *(rule)* Do not paste raw HTML beyond the allowed inline tags;
   anything structural belongs in Markdown.
