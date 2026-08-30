---
title: GUI Design
type: reference
tags: [conventions, development, gui, ux]
status: accepted
created: 2026-08-24
updated: 2026-08-30
---

# GUI Design

Applies to every GUI delivery - see
[`09-packaging-desktop.md`](09-packaging-desktop.md) for packaging
tracks. Decide **delivery mode** and **interaction profile** separately.
A browser-delivered application can still be a compact, keyboard-heavy
productivity tool.

## Delivery and interaction profile

Delivery describes where the interface runs, not how spacious it is:

| Delivery | Typical characteristics |
|---|---|
| **Desktop shell** | Installed beside local files, native window integration, commonly one user |
| **Browser** | Reached through a URL, potentially shared state, responsive across available viewports |

Choose the interaction profile from the work users perform:

| Profile | Use when | Default shape |
|---|---|---|
| **Productivity** | Repeated work over records, rules, files, messages, jobs, settings, or admin data | Compact app shell, keyboard and pointer efficient, high information density |
| **Reading / content** | Reading, reviewing, or presenting long-form content | Comfortable line length, calm navigation, more breathing room around content |
| **Overview / dashboard** | Monitoring summaries, trends, alerts, and exceptional conditions | Scannable status hierarchy and charts; drill-down leads to dense operational views |
| **Public / marketing** | Explaining or promoting a product to an unknown audience | Scroll-led narrative, responsive sections, deliberate whitespace |
| **Touch-first** | The primary workflow happens on phones, tablets, or coarse pointers | Larger targets, fewer simultaneous controls, progressive disclosure |

**Deciding rules of this chapter:**

1. *(default)* Record the interaction profile in the project README or
   design notes. Delivery alone never selects it.
2. *(default)* Productivity is the default for applications that manage
   structured items or repeated operations, including browser-based admin
   tools. Do not call such an application a dashboard merely because it
   has a web frontend.
3. *(default)* One responsive application may use a productivity profile
   on a wide fine-pointer viewport and a touch-first adaptation on a narrow
   or coarse-pointer viewport.
4. *(default)* When database-like operations are involved (structured
   records, shared or concurrent state), develop dockerized-web-first and
   wrap the same frontend for desktop use where a desktop shell adds value.
   This delivery choice does not change the interaction profile.

Sections below are marked *(desktop)*, *(web)*, *(Tk)*, or *(web-tech)*;
unmarked rules apply to every delivery.

## Principles

1. **Keyboard-efficient productivity** *(default)* - every productivity
   action is reachable without the mouse. Reuse established desktop command
   semantics where the host permits it: undo/redo, copy/paste, delete, and
   `Esc` to close or cancel. Desktop shells follow platform conventions;
   browser delivery never overrides browser or operating-system shortcuts.
   App-specific and single-key bindings apply only inside an explicitly
   focused workspace and never while the user is typing in an editable control.
2. **Adapt targets to input** *(default)* - start from the chosen component
   framework's density and sizing system, then adapt it to the interaction
   profile and actual input methods. Fine-pointer productivity views stay
   compact; touch-first views provide comfortable targets. Hover may reinforce
   an affordance but never carries required information.
3. **Minimal chrome, density by profile** *(default)* - content is the
   interface: thin topbars, compact toolbars, panes, tabs, and tables over
   card stacks and dialog mazes. Productivity views keep common data and
   controls visible without scrolling past introductory or setup content.
   Reading, overview, and public profiles may use more whitespace where it
   improves their actual task.
4. **Declarative before scripted** *(default)* - prefer what the
   platform expresses natively (semantic HTML, CSS, built-in widgets,
   standard library) over JavaScript or framework re-implementations of
   the same behavior. Script only the parts the platform cannot express.
5. **Instant feedback** *(default)* - previews render on selection,
   filters apply while typing, background work shows a persistent status
   indicator - never a frozen window.
6. **States are designed** *(default)* - no blank screens: loading shows
   skeletons/spinners, empty data shows a helpful empty state with the
   next action, errors render inline near their cause.
7. **First-run works** *(default)* - a fresh install is usable without
   setup: sensible defaults everywhere, setup flows only for decisions
   that genuinely need the user.
8. **Automatable by design** *(default)* - an app's operations are
   drivable without its GUI: a headless CLI (where it makes sense) plus
   an automation API (HTTP for served apps; an importable core
   otherwise). The GUI is one client among several, never the only
   interface - which forces business logic into a core that all shells
   share.
9. **Vendored assets** *(rule)* - no CDN fonts, icon packs, or script
   includes; vendor everything or use system stacks. Web-first apps
   additionally tolerate slow links: no megabyte heroes, lazy-load
   media.
10. **Local-first & installable** *(web, default)* - core function works
   **offline after first load**: app shell and assets are cached
   (service worker), cached content stays readable without connectivity,
   and locally entered data persists on the device until a real backend
   justifies sync. Regular-use web apps ship installable manifests -
   name, identity icon, standalone display - so they land on the home
   screen like native apps. Connectivity is an enhancement, never a
   prerequisite for the UI itself.
11. **State persists** *(desktop, default)* - window geometry, panel
   sizes, open document, scroll position, and theme survive relaunch
   (sidecar JSON / profile file). Web-first persists per account what
   the task implies (drafts, view options).
12. **Undo beats confirmation** *(default)* - prefer reversible actions
   with undo over confirm-dialog spam; true destructive ops confirm
   explicitly.

## Visual tokens *(web-tech)*

All look-and-feel values live as CSS custom properties on `:root`;
themes switch tokens only via `[data-theme]` attributes - components
never hardcode colors.

### Themes (optional feature)

Theming is not mandatory; ship it when users benefit from it. Worked-example shape:

- tokens grouped under `[data-theme="light"]`, `[data-theme="dark"]`,
  ..., each block also setting `color-scheme`
- a follow-system variant resolves via `prefers-color-scheme`
- adding a new standard theme later = appending one more attribute
  block; nothing else in the app changes

### Starter token set

Semantic names, extended per app as needed:

- surfaces: `--bg`, `--bg-elev`, `--bg-side`
- text: `--text`, `--text-dim`
- structure: `--border`
- accent: `--accent` + `--accent-soft` (derived via `color-mix()`)
- status: `--ok`, `--warn`, `--danger` (+ soft variants)
- content: `--mark`, `--mark-active`, `--code-bg`
- depth: `--shadow`

Accent/status soft variants derive from their base via `color-mix()` -
no second hardcoded palette anywhere.

### Type, spacing, fonts

- Fluid type scale: `clamp()`-based steps `--step--1 ... --step-4`
- Compact spacing scale based on 4px steps: 4, 8, 12, 16, and 24px;
  productivity screens rarely need larger internal gaps
- Separate control and container radii; controls stay tighter than panels
- Density tokens for control and row height derive from the chosen component
  framework, with profile-specific compact and touch-oriented variants
- rem-based sizing so OS text scaling works
- System font stacks: `ui-sans-serif / system-ui / Segoe UI ...` for UI,
  `ui-monospace ...` for code - no bundled webfonts unless branding
  genuinely requires it

## Interaction standards

- **Help overlay** *(desktop - rule for keyboard-driven apps)*: an always-visible
  Help command toggles an overlay listing **every** keybinding -
  **one command/key per line** (key column left, description right),
  grouped by task. Visually calm: no tables-with-borders, no animation,
  muted colors on the standard surface. If the list exceeds the parent
  window's vertical space, the overlay scrolls; it never resizes or
  reflows the app behind it. A shortcut may supplement the visible command only
  when it is host-safe and scoped outside editable controls. The overlay remains
  reachable from any state, including open panels. The same list is mirrored in
  the README; adding or changing a binding updates both in the same commit.
- **Search everywhere** *(default)*: any view over lists, tables, or item
  collections offers filter/highlight as-you-type with match count and visible
  next/previous controls; no reloads, no modals. Desktop shells may follow the
  platform's standard Find bindings. Browser delivery preserves browser Find
  and uses a visible app-search command plus a non-conflicting scoped binding
  where useful.
- **Media previews inline**: images/video/PDF/text render inside the
  pane (iframe/object/pre) instead of shelling out.
- **Drag & drop** *(desktop, default)* - apps whose subject is
   files/items accept them via drag & drop onto the workspace; drop
   targets indicate themselves visually during hover (highlighted
   panels, insertion markers). Web-first accepts drops where the browser
   allows it, but never relies on them.
- **Errors inline**, near their cause; reserve dialogs for decisions,
  not notifications.
- *(Tk)* Preserve established visual language, glyphs, and tab order
  during refactors (established-visual-language rule); long operations
  run off the main thread
  with progress + cancel.

## Productivity components *(default)*

Use this priority order for structured, repeated work:

1. **Collections: table before cards.** Repeated records with comparable
   fields use a semantic table. Less regular records use a compact divided
   list. A card per record is the last choice, reserved for items whose
   contents genuinely have different structures.
2. **Tabs for peer views.** Use tabs for a small set of views at the same
   level, such as Rules / Preview / History. Keep global navigation separate.
3. **Progressive disclosure for secondary detail.** Use `<details>`,
   expandable rows, drawers, or side panes for raw payloads, advanced fields,
   preview tools, and infrequent forms. Do not make every option permanently
   consume page height.
4. **Compact toolbars.** Put search, filters, sorting, selection actions,
   and the primary create action immediately above the collection. Avoid
   explanatory page introductions when labels and help text already explain
   the task.
5. **Forms follow task frequency.** A form that is the page's main task may
   remain open. A create or edit form beside a primary collection opens
   inline, in a drawer, or in a compact pane and closes after completion.
6. **Row actions use icons.** Familiar repeated actions such as edit, enable,
   preview, copy, and delete use compact icon buttons with an accessible name
   and tooltip. Show at most two common actions directly; move the rest into
   an overflow menu. Primary page actions and unfamiliar consequential
   actions retain visible text.
7. **Cards need a reason.** Use a card only when its boundary communicates
   grouping, selection, or elevation. Do not wrap every section, form, or
   list row in a large rounded container.
8. **Hierarchy before whitespace.** Establish hierarchy with alignment,
   typography, dividers, column structure, and restrained surface changes
   before increasing padding or separating content into cards.

### Tables and large collections

1. **One item per row** *(default)* - a structured collection renders one
   record per table row, with stable columns for comparable fields. Secondary
   prose or raw values expand from the row instead of turning every item into
   a form-sized block.
2. **Sortable where meaningful** *(default)* - columns users compare or use
   to find records are sortable from their headers. Show the active direction,
   preserve it across refreshes, and expose it with `aria-sort`. Do not add
   sorting to action or free-form detail columns.
3. **Pagination is operable** *(rule)* - if the interface shows only part of
   a result set **and the user cannot reasonably view the full set** (e.g.,
   unbounded search results, large catalogs), it also provides controls to
   reach the rest. Show the visible range and total, previous/next controls,
   and either page selection or an explicit load-more control. Search is not
   a substitute for pagination. Preserve filters and sorting while moving
   between pages; mark the current page with `aria-current` and disable
   unavailable directions.
4. **Scrollable tables for live sets** *(default)* - a bounded, live-updating
   dataset whose sort/filter applies to the full set is better shown as a
   scrollable table (`max-height` with simple overflow, or virtual scrolling)
   than paginated, which breaks the live-update flow. Show a total count and
   visible range ("1-47 of 47") in the toolbar. If the set can grow unbounded,
   add pagination or virtual scrolling to cap DOM size.
5. **Multi-selection for shared actions** *(default)* - when an operation can
   sensibly apply to several records, add a leading checkbox column, a header
   checkbox, and a bulk-action toolbar. Distinguish "select this page" from
   "select all filtered results" and state the selected count. Show a
   task-relevant aggregate, such as the selected balance, when it helps users
   verify the set. Keep single-row actions available without requiring
   selection.
6. **Actions have fixed homes** *(default)* - collection actions and bulk
   actions live in the toolbar above the table; per-record actions live in a
   consistently aligned trailing column; pagination sits directly below the
   collection and may repeat above very long tables. Account- or page-level
   actions belong in the page header or a dedicated settings section, never
   scattered between records.
7. **Inline editing stays inline** *(default)* - editable cells either save
   immediately with visible feedback or expose compact Save/Cancel actions in
   the edited row. Never place a full-width control and a separate Save button
   under every record. Multi-row edits use selection plus a bulk editor.
8. **Wide rows stay compact** *(default)* - keep core fields on one line in
   wide productivity tables. Truncate with an accessible full-value path or
   disclose secondary prose from the row rather than letting common columns
   wrap every record into a tall block.
9. **Narrow layouts preserve the working set** *(default)* - hide secondary
   columns behind an expandable row, or allow a constrained horizontal table
   scroll with the identifying column kept visible. Do not convert every row
   into a tall card merely because the viewport narrowed.
10. **Numeric columns support comparison** *(default)* - right-align quantities,
   currency, and other comparable numbers and use tabular figures
   (`font-variant-numeric: tabular-nums`) so digits remain vertically aligned.

## Icons *(web-tech)*

- House default: **Lucide**, vendored as individual inline SVGs under
  `vendor/icons/` - inline SVG inherits `currentColor`, so icons theme
  themselves with `--text`/`--accent` automatically.
- Font Awesome (self-hosted, never CDN) is the approved fallback when
  brand logos or exotic pictograms are needed; its CC-BY attribution
  goes into `THIRD_PARTY_NOTICES.md`.
- Every icon is labeled: `aria-label` when interactive, `aria-hidden`
  when decorative. Tk uses raster assets via `iconphoto`/`PhotoImage`.
- **App identity** *(default)*: every GUI app gets one identifying mark.
  It anchors the **top-left of the app's top bar** and doubles as the
  desktop/window icon (`iconphoto`/`PhotoImage` on Tk, window icon in
  pywebview, `.ico` via the PyInstaller spec for packaged builds). One
  master asset (SVG or high-res PNG) derives all sizes - never diverging
  copies. Test the derived mark at its smallest real target, such as a
  16px favicon or window icon; simplify it when its identifying geometry
  no longer survives.

## Layout patterns

- **Use available width by default**: app shells fill the available browser
  viewport or desktop window, so panes, tables, and workspaces can use wide
  displays. Desktop users may resize the window; persist that geometry. This
  does not require reading/content text columns to span the full shell - limit
  their measure where readability needs it.
- **Pane-based** house shape: resizable, collapsible side panel(s) +
  content area; sizes remembered per session (`--left-panel-w`,
  `--resize-w` handles at 5px hit width).
- **List-detail** productivity shape: a table or compact list owns the main
  view; selection reveals detail in an adjacent pane or expandable row
  without navigating away from the working set.
- **Collection-first ordering**: filters and records appear before preview,
  setup, diagnostics, or raw data unless one of those is the page's primary
  task.
- **Responsive collapse**: below a breakpoint (~860px) panels start
  hidden and toggle via explicit buttons - content wins space.
- Prefer one window with panes over many windows; wizards only for
  genuinely sequential setup flows.

## Component framework defaults *(pattern)*

Frameworks are implementation starting points, not visual dependencies. The
interaction, accessibility, density, and collection contracts in this chapter
remain authoritative:

- **Overview / dashboard** - start with
  [shadcn/ui](https://ui.shadcn.com/docs) and adapt its components to the
  project's visual language and interaction profile. Add
  [TanStack Table](https://tanstack.com/table/latest/docs/overview) when a
  collection needs advanced sorting, filtering, pagination, selection, or
  column state.
- **Productivity** - start with
  [Fluent UI React v9](https://react.fluentui.dev/). Use its
  [DataGrid](https://react.fluentui.dev/?path=/docs/components-datagrid--docs)
  for table-like keyboard interaction and select composite focus when arrow-key
  row navigation is required.

Use one component system per application. Record the choice and deliberate
deviations in the project's README or design notes, and verify the result at the
real target viewport and input method.

## Desktop toolkit notes *(historical input - adopt selectively)*

**No toolkit is house-mandated.** Simple shells skip native toolkits
entirely (pywebview over a static frontend - the newest small apps
needed none). Dense apps choose a toolkit per app and document the
choice in their README. Note: large Tkinter apps commonly outgrow it
toward richer toolkits (e.g., PySide6) - weigh that migration risk when choosing.
For reference only: what a mature Tkinter codebase
converged on, mostly transferable to any single-threaded UI toolkit:

- **(rule, when on Tk) Main-thread marshaling** - widgets are touched
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

1. Tooltips supplement visible labels, or explain familiar icon-only actions
   in repeated productivity controls. Every icon-only action still has an
   accessible name; its meaning never exists only on hover.
2. Short and stable: one short sentence max; no interactive content
   inside a tooltip.
3. Buttons with keybindings include the binding in their tooltip
   (`Paste path (Ctrl+V)`); the help overlay stays the complete
   reference.
4. Critical or urgent information never lives in a tooltip.
5. *(web-tech)* Native `title` attributes for lightweight hints;
   custom-styled tooltip components only when styling genuinely demands
   it, and they must appear on keyboard focus too, not just hover.
6. **Open delay ~200 ms** *(default)* - a hover is never intentional by
   itself; cursors cross triggers in transit. Below ~150 ms the tooltip
   fires during casual travel; above ~250 ms an intentional hover feels
   broken. Leaving the trigger before the delay elapses cancels the open
   entirely - sweeping the page opens nothing.
7. **Warm-window skip** *(default)* - when a tooltip closes, keep the
   surface *warm* for ~300 ms: hovering the next trigger inside that
   window opens **instantly, skipping the entrance animation**, because
   moving between related triggers *is* deliberate. Every open resets
   the cooldown; expiry returns the surface to cold and the ~200 ms wait
   applies again. Close delay stays 0 ms. Keyboard focus shows tooltips
   immediately (no delay) - focus is always intentional.
8. **Prefer declarative implementations** *(web-tech, default)* - the
   whole pattern works **without JavaScript**: `popover="hint"` +
   `interestfor` with CSS anchor positioning (`position-area`,
   `position-try` edge flips) and `interest-delay-start` /
   `interest-delay-end` for delay and warm-window (the warm state via
   `.area:has(:popover-open) { interest-delay-start: 0s }`). Wrap in
   `@supports not (interest-delay-start: 0s)` fallbacks where support
   lags. Script only what the platform cannot express.
9. *(Tk)* Use one shared tooltip helper (a shared tooltip-helper module
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
- Treating every browser application as a spacious dashboard or mobile-first
  landing page.
- One large card per record where a table or compact divided list would expose
  more information and support comparison.
- Full-width text buttons repeated on every row; use compact icon buttons with
  accessible names and an overflow menu.
- Oversized headings, controls, gaps, and mobile touch targets on wide
  fine-pointer productivity layouts.
- Permanent create, preview, or advanced-settings panels pushing the primary
  collection below the fold.
- Truncating a result set with text such as "showing 50 of 1707" but no way to
  reach the remaining records.
- Tables without meaningful sorting, or repeated records without
  multi-selection when the same action commonly applies to several items.
- Row, bulk, account, and navigation actions mixed into an unaligned stack of
  text buttons.
- Component frameworks/heavy UI libs for what ~200 lines of vanilla
  HTML/CSS/JS do (a three-pane tool ships fine with zero UI dependencies).
- Telemetry, update pings, remote embedding calls, or other silent network
  traffic in local-first tools. Such calls need a documented feature and an
  explicit user choice.
