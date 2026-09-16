---
title: Markdown Flavor
type: reference
tags: [conventions, wiki, markdown]
status: accepted
created: 2026-08-24
updated: 2026-09-16
---

# Markdown Flavor

House dialect: [CommonMark](https://spec.commonmark.org/) + [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) **plus** the
extensions our toolchain renders natively (the Markview set at
https://git.kaiuweneumann.de/kai/MarkdownViewer). Write
within this dialect so every consumer - the editor, Markview,
Forgejo/GitHub - shows the note as intended.

Reference implementation is the vendored Markview frontend:
`markdown-it` with `html: true, linkify: true, typographer: true, breaks: false`
plus `alert`, `emoji`, `footnote`, `sub`, `sup`, `task-lists`,
custom `==mark==` (`<mark>`), KaTeX for `$...$` and `$$...$$`,
Mermaid for ` ```mermaid ` fences, highlight.js, Obsidian-style image
sizes (`![alt|400]`), and DOMPurify
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
| Image sizes | `![alt|400]` / `![alt|400x250]` | literal pipe suffix in alt text |

Frontmatter stays YAML per [`01-frontmatter.md`](01-frontmatter.md)
and is rendered as a metadata table when present. A leading block
delimited by `---` / `---` or `---` / `...` is accepted.

## Image sizes

*(default)* Images accept an Obsidian-style size suffix in the alt
text. `![Diagram|400](diagram.png)` renders 400 pixels wide;
`![Photo|400x250](photo.jpg)` sets width and height. Plain renderers
show the suffix as literal alt text, so keep the description readable
with the suffix attached.

Markview applies the size in the live preview. For Pandoc output the
same syntax converts through this Lua filter, stored beside the
build as `obsidian-image-size.lua`:

```lua
-- Convert Obsidian-style image dimensions in Markdown alt text to Pandoc-- image attributes.
--
-- Supported source syntax:
--   ![Description|400](image.svg)
--   ![Description|400x250](image.svg)
--
-- Resulting Pandoc attributes are equivalent to:
--   ![Description](image.svg){width=400px}
--   ![Description](image.svg){width=400px height=250px}
--
-- Usage:
--   pandoc input.md --lua-filter=obsidian-image-size.lua -o output.pdf
--
-- Notes:
--   * Dimensions must be positive integers and are interpreted as pixels.
--   * Ordinary images and alt text containing non-size pipes are unchanged.
--   * This handles standard Markdown images using Obsidian's alt-text sizing.
--     It does not handle Obsidian wikilink embeds such as ![[image.svg|400]].


local function split_caption_and_size(caption)
  local text = pandoc.utils.stringify(caption)


  local alt, width, height = text:match("^(.-)|(%d+)%s*[xX]%s*(%d+)%s*$")
  if not width then
    alt, width = text:match("^(.-)|(%d+)%s*$")
  end


  if not width then
    return nil
  end


  width = tonumber(width)
  height = height and tonumber(height) or nil
  if width == 0 or height == 0 then
    return nil
  end


  return alt, width, height
end


function Image(image)
  local alt, width, height = split_caption_and_size(image.caption)
  if not alt then
    return nil
  end


  image.caption = { pandoc.Str(alt) }
  image.attributes.width = tostring(width) .. "px"
  if height then
    image.attributes.height = tostring(height) .. "px"
  end


  return image
end


-- With Pandoc's implicit_figures extension, a paragraph containing only an
-- image becomes a Figure. Pandoc copies the original image caption into the
-- figure caption before filters run, so remove the size suffix there as well.
function Figure(figure)
  local alt = split_caption_and_size(figure.caption.long)
  if not alt then
    return nil
  end


  figure.caption.long = { pandoc.Plain({ pandoc.Str(alt) }) }
  return figure
end
```

Usage:

```bash
pandoc input.md --lua-filter=obsidian-image-size.lua -o output.pdf
```

Dimensions must be positive integers and count as pixels. Alt text
with non-size pipes stays unchanged. Obsidian wikilink embeds such
as `![[image.png|400]]` are out of scope.

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
