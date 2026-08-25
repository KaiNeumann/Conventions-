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
| Runs | installed shell next to the user's files (pywebview/Tkinter) | in a browser tab, reached over a network |
| Audience | the power user who chose it, daily | mixed, unknown, often phones |
| Session shape | long, high-frequency operations | short, task-oriented visits |
| Primary input | keyboard-first | touch & pointer first |
| Data & persistence | local files on one machine; single writer | structured/shared state; DB-like operations |
| Examples | local file/document tools, readers | community sites, admin consoles |

**Deciding rules of this chapter:**

1. The class applies **per deployment**: one codebase can ship both
   variants (same frontend installed as shell and served in a browser),
   and each delivery follows its own class rules.
2. Ambiguous audience ⇒ treat it as **web-first** (anything served over
   a network to people other than today's user).
3. **Default development strategy**: when database-like operations are
   involved (structured records, shared or concurrent state), develop
   **dockerized-web-first** and wrap the very same frontend for desktop
   use (pywebview) where a desktop shell adds value. Purely local,
   file-centric tools may start desktop-first.

Sections below are marked *(desktop)*, *(web)*, *(Tk)*, or *(web-tech)*;
unmarked rules apply to both classes.

## Principles

1. **Keyboard-first** *(desktop-first deployments)* — every action
   reachable without the mouse: single keys for high-frequency operations
   (e.g., number/letter keys to file or step through items), `Ctrl+`
   combos for meta actions, `Esc` closes/cancels. Every binding is
   listed in the help overlay (see below) and mirrored in a README table.
2. **Touch & pointer first** *(web-first deployments)* — every primary
   action works one-handed on a phone: hit targets ≥ 44px, visible text
   labels over icon-only buttons, hover never carries information, and
   bare single-key handlers exist only inside explicitly focused shortcut
   scopes (never global page listeners fighting the browser).
3. **Minimal chrome, density by app type** *(default)* — content is the
   interface: thin topbars, pane layouts over dialog mazes. **Dashboard-
   style web apps may scroll with generous whitespace. Workflow-driven
   apps aim for desktop-GUI information density**: compact views,
   controls visible without scrolling — attempted in web UIs just as in
   native ones.
4. **Instant feedback** *(default)* — previews render on selection,
   filters apply while typing, background work shows a persistent status
   indicator — never a frozen window.
5. **States are designed** *(default)* — no blank screens: loading shows
   skeletons/spinners, empty data shows a helpful empty state with the
   next action, errors render inline near their cause.
6. **First-run works** *(default)* — a fresh install is usable without
   setup: sensible defaults everywhere, setup flows only for decisions
   that genuinely need the user.
7. **Automatable by design** *(default)* — an app's operations are
   drivable without its GUI: a headless CLI (where it makes sense) plus
   an automation API (HTTP for served apps; an importable core
   otherwise). The GUI is one client among several, never the only
   interface — which forces business logic into a core that all shells
   share.
8. **Vendored assets** *(rule)* — no CDN fonts, icon packs, or script
   includes; vendor everything or use system stacks. Web-first apps
   additionally tolerate slow links: no megabyte heroes, lazy-load
   media.
9. **State persists** *(desktop, default)* — window geometry, panel
   sizes, open document, scroll position, and theme survive relaunch
   (sidecar JSON / profile file). Web-first persists per account what
   the task implies (drafts, view options).
10. **Undo beats confirmation** *(default)* — prefer reversible actions
   with undo over confirm-dialog spam; true destructive ops confirm
   explicitly.

## Visual tokens *(web-tech)*

All look-and-feel values live as CSS custom properties on `:root`;
themes switch tokens only via `[data-theme]` attributes — components
never hardcode colors.

### Themes (optional feature)

Theming is not mandatory; ship it when users benefit from it. Worked-example shape:

- tokens grouped under `[data-theme="light"]`, `[data-theme="dark"]`,
  …, each block also setting `color-scheme`
- a follow-system variant resolves via `prefers-color-scheme`
- adding a new standard theme later = appending one more attribute
  block; nothing else in the app changes

### Starter token set

Semantic names, extended per app as needed:

- surfaces: `--bg` · `--bg-elev` · `--bg-side`
- text: `--text` · `--text-dim`
- structure: `--border`
- accent: `--accent` + `--accent-soft` (derived via `color-mix()`)
- status: `--ok` · `--warn` · `--danger` (+ soft variants)
- content: `--mark` · `--mark-active` · `--code-bg`
- depth: `--shadow`

Accent/status soft variants derive from their base via `color-mix()` —
no second hardcoded palette anywhere.

### Type, spacing, fonts

- Fluid type scale: `clamp()`-based steps `--step--1 … --step-4`
- One spacing var (`--space`) and one radius var (`--radius`)
- rem-based sizing so OS text scaling works
- System font stacks: `ui-sans-serif / system-ui / Segoe UI …` for UI,
  `ui-monospace …` for code — no bundled webfonts unless branding
  genuinely requires it

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
- **Search everywhere** *(default)*: any view over lists, tables, or item collections offers filter/highlight as-you-type with match count and
  next/previous navigation (`F3`/`Shift+F3`); no reloads, no modals.
- **Media previews inline**: images/video/PDF/text render inside the
  pane (iframe/object/pre) instead of shelling out.
- **Errors inline**, near their cause; reserve dialogs for decisions,
  not notifications.
- *(Tk)* Preserve established visual language, glyphs, and tab order
  during refactors (established-visual-language rule); long operations
  run off the main thread
  with progress + cancel.

## Icons *(web-tech)*

- House default: **Lucide**, vendored as individual inline SVGs under
  `vendor/icons/` — inline SVG inherits `currentColor`, so icons theme
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
  hidden and toggle via explicit buttons — content wins space.
- Prefer one window with panes over many windows; wizards only for
  genuinely sequential setup flows.

## Desktop toolkit notes *(historical input — adopt selectively)*

**No toolkit is house-mandated.** Simple shells skip native toolkits
entirely (pywebview over a static frontend — the newest small apps
needed none). Dense apps choose a toolkit per app and document the
choice in their README. Note: large Tkinter apps commonly outgrow it
toward richer toolkits (e.g., PySide6) — weigh that migration risk when choosing.
For reference only: what a mature Tkinter codebase
converged on, mostly transferable to any single-threaded UI toolkit:

- **(rule, when on Tk) Main-thread marshaling** — widgets are touched
  only on the UI thread via an executor (`call`, `debounce`,
  `cancel`) pumping a cross-thread queue; workers post events, never
  touch widgets. Every mainstream toolkit has an equivalent rule.
- *(pattern)* Light/dark theming following the OS, driven by one
  semantic palette dict in a shared module; popups themed through a
  helper.
- *(pattern)* User font-size deltas relative to the theme baseline, so
  switches never compound.
- *(pattern)* Toasts near the triggering point; statusbar counters;
  inline validation over modal spam.
- *(pattern)* Modals centered over their parent, clamped to screen
  bounds.
- *(pattern)* Settings forms generated from a spec shared with the CLI.
- *(pattern)* Reusable widgets live in a shared package so sibling apps
  stay visually consistent.

## Tooltips *(default)*

1. Tooltips **supplement labels, never replace them** — anything that
   exists only on hover is invisible on touch screens and to keyboard
   users.
2. Short and stable: one short sentence max; no interactive content
   inside a tooltip.
3. Buttons with keybindings include the binding in their tooltip
   (`Paste path (Ctrl+V)`); the help overlay stays the complete
   reference.
4. Critical or urgent information never lives in a tooltip.
5. *(web-tech)* Native `title` attributes for lightweight hints;
   custom-styled tooltip components only when styling genuinely demands
   it, and they must appear on keyboard focus too, not just hover.
6. *(Tk)* Use one shared tooltip helper (a shared tooltip-helper module
   pattern) so timing and styling stay consistent app-wide.

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
  HTML/CSS/JS do (a three-pane tool ships fine with zero UI dependencies).
- Telemetry, update pings, or network calls in offline tools.
