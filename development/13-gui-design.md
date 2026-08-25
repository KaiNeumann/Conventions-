---
title: GUI Design
type: reference
tags: [conventions, development, gui, ux]
status: draft
created: 2026-08-24
updated: 2026-08-24
---

# GUI Design

Applies to GUI work of both kinds — see
[`08-packaging-desktop.md`](08-packaging-desktop.md) for packaging
tracks. First decide the **app class**; it changes the interaction
model more than any framework choice.

## App class decides

| | **Desktop-first** | **Web-first** |
|---|---|---|
| Runs | installed shell next to the user's files (pywebview/Qt) | in a browser tab, reached over a network |
| Audience | the power user who chose it, daily | mixed, unknown, often phones |
| Session shape | long, high-frequency operations | short, task-oriented visits |
| Primary input | **keyboard-first** | **touch & pointer first** |
| Examples | organizer, markdownviewer, RAT | GoldsteinCMS, ScraperCMS UI |

Sections below are marked *(desktop)*, *(web)*, *(Qt)*, or *(web-tech)*;
unmarked rules apply to both classes.

## Principles

1. **Keyboard-first** *(desktop, default)* — every action reachable
   without the mouse: single keys for high-frequency operations
   (organizer: `1`–`0`/`a`–`z` to file items), `Ctrl+` combos for meta
   actions, `Esc` closes/cancels. Every binding is listed in the help
   overlay (see below) and mirrored in a README table.
2. **Touch & pointer first** *(web, default)* — every primary action
   works one-handed on a phone: hit targets ≥ 44px, visible text labels
   over icon-only buttons, hover never carries information, and bare
   single-key handlers exist only inside explicitly focused shortcut
   scopes (never global page listeners fighting the browser).
3. **Minimal chrome** *(default)* — content is the interface: thin
   topbars, pane layouts over dialog mazes, no decorative headers.
4. **Instant feedback** *(default)* — previews render on selection,
   filters apply while typing, background work shows a persistent status
   indicator — never a frozen window.
5. **Vendored assets** *(rule)* — no CDN fonts, icon packs, or script
   includes; vendor everything or use system stacks. Web-first apps
   additionally tolerate slow links: no megabyte heroes, lazy-load
   media.
6. **State persists** *(desktop, default)* — window geometry, panel
   sizes, open document, scroll position, and theme survive relaunch
   (sidecar JSON / profile file). Web-first persists per account what
   the task implies (drafts, view options).
7. **Undo beats confirmation** *(default)* — prefer reversible actions
   with undo over confirm-dialog spam; true destructive ops confirm
   explicitly.

## Visual tokens *(web)*

All look-and-feel values live as CSS custom properties on `:root`;
themes switch tokens only via `[data-theme]` attributes — components
never hardcode colors.

- **Semantic names**: `--bg --bg-elev --bg-side --text --text-dim
  --border --accent --accent-soft --mark --code-bg --shadow`
  (markdownviewer set is the reference implementation).
- **Mandatory themes**: light and dark, plus follow-system; extras
  optional (e.g. sepia). Each sets `color-scheme`.
- **Accent variants** derive from `--accent` via `color-mix()` for
  soft/hover/selection states — no second hardcoded palette.
- **Fluid type scale**: `clamp()`-based `--step--1 … --step-4` plus one
  spacing var and one radius var; rem-based so OS text scaling works.
- **System font stacks**: `ui-sans-serif/system-ui…` for UI,
  `ui-monospace…` for code — no bundled webfonts unless a brand
  requires it.

## Interaction standards

- **Help overlay** *(desktop — rule for keyboard-driven apps)*: `?`
  toggles an always-available overlay listing **every** keybinding —
  **one command/key per line** (key column left, description right),
  grouped by task. Visually calm: no tables-with-borders, no animation,
  muted colors on the standard surface. If the list exceeds the parent
  window's vertical space, the overlay scrolls; it never resizes or
  reflows the app behind it. Reachable from any state, including open
  panels. The same list is mirrored in the README; adding or changing a
  binding updates both in the same commit.
- **Search**: filter/highlight as-you-type with match count and
  next/previous navigation (`F3`/`Shift+F3`); no reloads, no modals.
- **Media previews inline**: images/video/PDF/text render inside the
  pane (iframe/object/pre) instead of shelling out.
- **Errors inline**, near their cause; reserve dialogs for decisions,
  not notifications.
- *(Qt)* Preserve established visual language, glyphs, and tab order
  during refactors (RAT rule); long operations run off the main thread
  with progress + cancel.

## Icons

- House default: **Lucide**, vendored as individual inline SVGs under
  `vendor/icons/` — inline SVG inherits `currentColor`, so icons theme
  themselves with `--text`/`--accent` automatically.
- Font Awesome (self-hosted, never CDN) is the sanctioned fallback when
  brand logos or exotic pictograms are needed; its CC-BY attribution
  goes into `THIRD_PARTY_NOTICES.md`.
- Every icon is labeled: `aria-label` when interactive, `aria-hidden`
  when decorative. Qt uses the same SVG files via `QIcon`.

## Layout patterns

- **Pane-based** house shape: resizable, collapsible side panel(s) +
  content area; sizes remembered per session (`--left-panel-w`,
  `--resize-w` handles at 5px hit width).
- **Responsive collapse**: below a breakpoint (~860px) panels start
  hidden and toggle via explicit buttons — content wins space.
- Prefer one window with panes over many windows; wizards only for
  genuinely sequential setup flows.

## Native track specifics *(Qt)*

- Dense, data-centric layouts are welcome (queues, tables, settings
  trees) — match RAT: tabs per concern, statusbar counters, global speed
  limits visible in the chrome.
- Settings persist to portable INI/YAML beside the executable or in the
  profile dir; the GUI reads/writes the same file the CLI uses — one
  settings truth.

## Accessibility baseline *(rule)*

- Visible focus indicators on all interactive elements; full keyboard
  traversal without traps.
- Text contrast meets WCAG AA in **every shipped theme**.
- Respect `prefers-reduced-motion`; animations enhance, never carry
  information alone.

## Anti-patterns

- Confirm-dialog spam, wizard-for-a-single-field, modal error popups for
  recoverable issues.
- Component frameworks/heavy UI libs for what ~200 lines of vanilla
  HTML/CSS/JS do (organizer ships a three-pane app with zero deps).
- Telemetry, update pings, or network calls in offline tools.
