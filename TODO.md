# TODO

Work queue per [`development/16-work-tracking.md`](development/16-work-tracking.md).

## Bugs

(none)

## Todos

- **[P1][DOCS][wiki] Accept remaining wiki chapters - IN PROGRESS**
  Done when: `03-editor-setup.md` and `06-dynamic-views.md` pass
  interactive review, `wiki/README.md` flips to accepted, and the
  release is tagged v1.2.0.
  Refs: wiki/03-editor-setup.md, wiki/06-dynamic-views.md

- **[P2][DOCS][agents] Review the agent communication protocol - OPEN**
  Adopted 2026-09-28 as `status: accepted`. Review at ~2026-10-28
  (first pass) and again at ~2026-12-28 (second pass).
  Done when: both reviews happened and the chapter was either left
  unchanged, reworded, or re-tiered, and the outcome was recorded in
  `CHANGELOG.md`. Check against section 13: has the protocol held, or
  did a specific rule fail often enough to be automated or dropped?
  Refs: agents/04-agent-communication-protocol.md

- **[P3][DOCS][agents] Reference the protocol from AGENTS.md.template - OPEN**
  The template does not yet link
  `agents/04-agent-communication-protocol.md`, so new repositories
  created from it do not pick the protocol up.
  Done when: the template points at the chapter and the point is
  recorded in `CHANGELOG.md`. Refs: agents/AGENTS.md.template,
  agents/04-agent-communication-protocol.md

## Ideas

- **Pre-push prose-style scan** (unrefined - run the banned-vocabulary
  grep from development/06-documentation.md as a hook so AI-tells never
  reach the forge)
