---
title: Markdown Flavor
type: reference
tags: [conventions, wiki, markdown]
status: accepted
created: 2026-08-24
updated: 2026-08-28
---

# Markdown Flavor

House dialect: CommonMark + GitHub-flavored Markdown **plus** the
extensions our toolchain renders natively (the Markview set at
https://git.kaiuweneumann.de/kai/MarkdownViewer). Write
within this dialect so every consumer - Obsidian, Markview,
Forgejo/GitHub - shows the note as intended.

Reference implementation is the vendored Markview frontend:
`markdown-it` with `html: true, linkify: true, typographer: true, breaks: false`
plus `alert`, `emoji`, `footnote`, `sub`, `sup`, `task-lists`,
custom `==mark==` (`<mark>`), KaTeX for `$...$` and `$$...$$`,
Mermaid for ` ```mermaid ` fences, highlight.js, and DOMPurify
(`mark` and `kbd` allowed, `target` and `aria-hidden` kept).

## Supported extensions

| Feature | Syntax | Degrades to (plain/Forgejo renderers) |
|---|---|---|
| Tables | GFM pipes | renders fine |
| Task lists | `- [ ]` / `- [x]` | renders fine |
| Strikethrough | `~~text~~` | renders fine |
| Alerts | `> [!NOTE]` `> [!TIP]` `> [!IMPORTANT]` `> [!WARNING]` `> [!CAUTION]` | plain blockquote |
| Footnotes | `[^1]` / `[^1]: text` | inline marker text |
| Emoji shortcodes | `:tada:` | literal text |
| Subscript | `~text~` (`H~2~O`) | literal tildes |
| Superscript | `^text^` (`x^2^`) | literal carets |
| Highlight | `==text==` → `<mark>` | literal equals signs |
| Keyboard keys | `<kbd>Ctrl</kbd>` | sanitized text |
| Math | `$...$` inline, `$$...$$` display (KaTeX) | literal dollars |
| Diagrams | ` ```mermaid ` fences | fenced code block |
| Linkify | bare URLs autolink | plain text |
| Typographer | smart quotes and dashes | plain ASCII |

Frontmatter stays YAML per [`01-frontmatter.md`](01-frontmatter.md)
and is rendered as a metadata table when present. A leading block
delimited by `---` / `---` or `---` / `...` is accepted.

## Rules

1. *(default)* Stay inside the dialect. An extension not listed above
   requires a change to this file first - and support in the rendering
   toolchain.
2. *(default)* Prefer constructs that degrade gracefully; the last
   column shows what plain renderers display instead.
3. *(rule)* Do not paste raw HTML beyond the allowed inline tags
   (`mark` and `kbd` and their closing tags); anything structural
   belongs in Markdown. Sanitization keeps only `mark`, `kbd`,
   `target`, and `aria-hidden`.
4. *(default)* For math, do not put spaces directly inside the
   delimiters (`$ x$` and `$x $` do not render as math by design,
   to avoid currency false positives).
