---
title: Archify Diagrams
type: reference
tags: [conventions, development, documentation, architecture, archify]
status: accepted
created: 2026-08-31
updated: 2026-08-31
---

# Archify Diagrams

Archify is an interactive-diagram alternative to Mermaid for projects that
need more than a static, in-Markdown diagram: explorable HTML with inline
SVG, theme switching, route tracing, guided stories, and crisp PNG/SVG/WebM
export. It is the "distribution-quality" member of the house diagram
family, not a replacement for the everyday Mermaid conventions in
[`18-architecture-diagrams.md`](18-architecture-diagrams.md).

## What Archify is, and when to reach for it *(pattern)*

Archify is an agent skill (Node.js renderer + JSON schema) that compiles a
typed JSON intermediate representation into a single self-contained HTML
file. The agent authors the JSON IR from a plain-language description or a
pasted Mermaid diagram; Archify validates it and renders the output with no
server, no dependencies, and no runtime.

Reach for it when the diagram is an artifact people will *explore and
share* outside the repository — a slide, a README hero, an onboarding map,
a PR review — rather than a diagram that must render inline in Markdown.
When you only need a diagram that lives in the repo's Markdown and renders
in its viewer, the Mermaid conventions in `18-architecture-diagrams.md`
remain the default.

- `Archify renders from JSON IR, not Mermaid. ` It accepts pasted Mermaid as
  *input*, but its own source of truth is typed JSON; it does not parse
  Mermaid back out. Do not treat an Archify artifact as a drop-in
  replacement for a Mermaid fence in Markdown.
- `Archify is not the everyday default. ` The portability and
  plain-Markdown stance of
  [`../README.md`](../README.md) and
  [`18-architecture-diagrams.md`](18-architecture-diagrams.md) still holds:
  a self-contained HTML file is not versionable-by-diff the way Mermaid
  source in a fence is. Adopt Archify per project, when the artifact
  warrants it.

The five diagram types — architecture, workflow, sequence, data-flow, and
lifecycle — map one-to-one onto the questions the Mermaid chapter already
separates. The same level, peer, and scope discipline applies; Archify
changes the rendering, not the thinking.

## Skill location and installation

The skill is vendored in the sibling
`agent-skills` collection at `skills/archify/` (MIT, vendor-pinned), so
both repositories stay self-contained and versioned. Install it by linking
or copying that folder into the consuming harness's skill path:

- OpenCode: `.opencode/skills/archify` (project) or
  `~/.config/opencode/skills/archify` (global).
- Other harnesses: any `SKILL.md`-capable loader reads the same folder
  directly.

The upstream project is [`tt-a1i/archify`](https://github.com/tt-a1i/archify)
(MIT license). When the vendored copy falls meaningfully behind and a
project needs a newer renderer, update the vendored folder from upstream
and record the version bump in `agent-skills` — do not let projects drift
on unpinned upstream.

## Authoring discipline *(pattern)*

The skill's own `SKILL.md` is the authoritative authoring contract and
wins over this summary. The points below are the house rules that keep
Archify output consistent with the rest of the conventions:

1. One diagram answers one stated question for one named audience, exactly
   as in `18-architecture-diagrams.md`. State level and audience in the
   surrounding prose before generating.
2. Prefer the bounded authoring path: pick the type, read its schema plus
   one example, write the candidate JSON, then `validate` after every edit
   and `deliver` for the final HTML. A `--quality showcase` pass is the
   acceptance bar (9 checks, 0 composition errors, 0 warnings).
3. Start sparse: one clear main path, short side branches, at most 12
   primary nodes. Do not pre-plan coordinates or add geometry controls
   (`via`, `channelX/Y`, `labelAt`) before a diagnostic calls for one.
4. Static output is the default; enable motion only when the user asks for
   a demo or presentation.
5. Do not rely on color alone; shape, boundary, and label must still
   distinguish categories, matching the accessibility stance of the Mermaid
   chapter.

## Compared to the Mermaid conventions *(pattern)*

| Concern | Mermaid (default) | Archify (opt-in) |
|---|---|---|
| Where it lives | Mermaid fence, in the Markdown beside the architecture | Standalone `.html` artifact |
| Source of truth | The fence text, diff-able | Typed JSON IR, diff-able |
| Renders where | Any Mermaid-capable viewer | Any browser, no server |
| Interaction | Static | Explore, routes, stories, themes, export |
| Versioning | In-repo, reviewable in PR diff | In-repo JSON + output artifact |
| Use when | Diagram stays in the repo's docs | Diagram is shared as a standalone object |

Neither supersedes the other. Keep the Mermaid source for anything that
must render in Markdown; produce an Archify artifact when the diagram is
itself the deliverable. When both are needed, they describe the same
architecture and must not drift apart — update the JSON IR and the Mermaid
fence in the same change that alters the architecture they depict.