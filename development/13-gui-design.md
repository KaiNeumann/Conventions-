---
title: GUI Design
type: reference
tags: [conventions, development, gui, ux]
status: draft
created: 2026-08-24
updated: 2026-08-24
---

# GUI Design

Applies to GUI work of both kinds â€” see
[`08-packaging-desktop.md`](08-packaging-desktop.md) for packaging
tracks. First decide the **app class**; it changes the interaction
model more than any framework choice.

## App class decides

| | **Desktop-first** | **Web-first** |
|---|---|---|
| Runs | installed shell next to the user's files (pywebview/Tkinter) | in a browser tab, reached over a network |
| Audience | the power user who chose it, daily | mixed, unknown, often phones |
| Session shape | long, high-frequency operations | short, task-oriented visits |
| Primary input | **keyboard-first** | **touch & pointer first** |
| Examples | organizer, markdownviewer, RAT | GoldsteinCMS, ScraperCMS UI |

Sections below are marked *(desktop)*, *(web)*, *(Tk)*, or *(web-tech)*;
unmarked rules apply to both classes.

## Principles

1. **Keyboard-first** *(desktop, default)* â€” every action reachable
   without the mouse: single keys for high-frequency operations
   (organizer: `1`â€“`0`/`a`â€“`z` to file items), `Ctrl+` combos for meta
   actions, `Esc` closes/cancels. Every binding is listed in the help
   overlay (see below) and mirrored in a README table.
2. **Touch & pointer first** *(web, default)* â€” every primary action
   works one-handed on a phone: hit targets â‰¥ 44px, visible text labels
   over icon-only buttons, hover never carries information, and bare
   single-key handlers exist only inside explicitly focused shortcut
   scopes (never global page listeners fighting the browser).
3. **Minimal chrome** *(default)* â€” content is the interface: thin
   topbars, pane layouts over dialog mazes, no decorative headers.
4. **Instant feedback** *(default)* â€” previews render on selection,
   filters apply while typing, background work shows a persistent status
   indicator â€” never a frozen window.
5. **Vendored assets** *(rule)* â€” no CDN fonts, icon packs, or script
   includes; vendor everything or use system stacks. Web-first apps
   additionally tolerate slow links: no megabyte heroes, lazy-load
   media.
6. **State persists** *(desktop, default)* â€” window geometry, panel
   sizes, open document, scroll position, and theme survive relaunch
   (sidecar JSON / profile file). Web-first persists per account what
   the task implies (drafts, view options).
7. **Undo beats confirmation** *(default)* â€” prefer reversible actions
   with undo over confirm-dialog spam; true destructive ops confirm
   explicitly.

## Visual tokens *(web)*

All look-and-feel values live as CSS custom properties on `:root`;
themes switch tokens only via `[data-theme]` attributes â€” components
never hardcode colors.

- **Semantic names**: `--bg --bg-elev --bg-side --text --text-dim
  --border --accent --accent-soft --mark --code-bg --shadow`
  (markdownviewer set is the reference implementation).
- **Mandatory themes**: light and dark, plus follow-system; extras
  optional (e.g. sepia). Each sets `color-scheme`.
- **Accent variants** derive from `--accent` via `color-mix()` for
  soft/hover/selection states â€” no second hardcoded palette.
- **Fluid type scale**: `clamp()`-based `--step--1 â€¦ --step-4` plus one
  spacing var and one radius var; rem-based so OS text scaling works.
- **System font stacks**: `ui-sans-serif/system-uiâ€¦` for UI,
  `ui-monospaceâ€¦` for code â€” no bundled webfonts unless a brand
  requires it.

## Interaction standards

- **Help overlay** *(desktop â€” rule for keyboard-driven apps)*: `?`
  toggles an always-available overlay listing **every** keybinding â€”
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
- *(Tk)* Preserve established visual language, glyphs, and tab order
  during refactors (RAT rule); long operations run off the main thread
  with progress + cancel.

## Icons

- House default: **Lucide**, vendored as individual inline SVGs under
  `vendor/icons/` â€” inline SVG inherits `currentColor`, so icons theme
  themselves with `--text`/`--accent` automatically.
- Font Awesome (self-hosted, never CDN) is the sanctioned fallback when
  brand logos or exotic pictograms are needed; its CC-BY attribution
  goes into `THIRD_PARTY_NOTICES.md`.
- Every icon is labeled: `aria-label` when interactive, `aria-hidden`
  when decorative. Tk uses raster assets via `iconphoto`/`PhotoImage`.

## Layout patterns

- **Pane-based** house shape: resizable, collapsible side panel(s) +
  content area; sizes remembered per session (`--left-panel-w`,
  `--resize-w` handles at 5px hit width).
- **Responsive collapse**: below a breakpoint (~860px) panels start
  hidden and toggle via explicit buttons â€” content wins space.
- Prefer one window with panes over many windows; wizards only for
  genuinely sequential setup flows.

## Native track specifics *(Tk)*

The production-proven native stack is **Tkinter/ttk with sv-ttk
theming**, hardened across RAT's 0.19.x line (PySide6 exists as an
experimental packaged target, never shipped to production).

- **Theming**: `sv-ttk` light/dark themes, following the OS via
  `darkdetect`; one semantic palette dict (`base_bg`, `entry_bg`,
  `border`, â€¦) in a shared theme module; popup windows get themed via a
  `apply_palette_to_popup` helper â€” never styled ad hoc.
- **Font scaling**: user font-size deltas apply relative to the current
  theme's baseline sizes, so switching themes never compounds.
- **Threading**: widgets are touched **only on the Tk main thread**,
  marshaled through a `UiExecutor` (`call`, `debounce(key, delay)`,
  `cancel`) that pumps a cross-thread queue; worker threads post events,
  never touch widgets directly. This is the single most important Tk
  rule.
- **Feedback components**: auto-dismissing toasts near the triggering
  point (~1.2 s, bottom-right fallback), statusbar counters, inline
  validation â€” no modal error spam (mirrors the web track).
- **Windowing**: modals center over their parent, clamped to screen
  bounds with sane minimums; window geometry persists per app.
- **Declarative settings forms**: UI forms are generated from a settings
  spec (spec â†’ form builder â†’ editor dialog); the GUI edits the same
  file the CLI reads â€” one settings truth.
- **Shared component library**: reusable panels/tables/tooltips live in
  `src/shared/ui/*` so sibling apps stay visually identical.

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
