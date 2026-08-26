---
title: MCP Servers
type: reference
tags: [conventions, agents, mcp]
status: draft
created: 2026-08-25
updated: 2026-08-25
---

# MCP Servers

Accepted Model Context Protocol servers - what agents
may use, why they earn their place, and how new ones get admitted.
Servers are provided through the agent harness configuration; no
per-project MCP setups exist today.

## Accepted servers

| Server | Provides | Why kept |
|---|---|---|
| `codegraph` | Code knowledge graph: symbols, call paths, blast radius per file | Query-before-read replaces grep/read loops - large token savings on every code task |
| `context7` | Up-to-date library documentation on demand | Stops hallucinated APIs; cheaper than web searches during coding |

## Admission criteria *(rule)*

A new server is added only when **all** hold:

1. A recurring need across sessions/projects, not a one-off task.
2. Actively maintained upstream; supply-chain risk reviewed (what the
   server can reach: files, network, credentials).
3. Data boundary respected: prefer local stdio servers; remote/SaaS
   endpoints must never receive private repository content without an
   explicit decision.
4. Permission footprint understood and acceptable.
5. Token economics positive: the context/results it returns must cost
   less than the alternative.

| Server | Provides | Why kept |
|---|---|---|
| `codegraph` | Code knowledge graph: symbols, call paths, blast radius per file | Query-before-read replaces grep/read loops - large token savings on every code task |
| `context7` | Up-to-date library documentation on demand | Stops hallucinated APIs; cheaper than web searches during coding |
| `playwright` *(project-scoped)* | Browser automation: navigation, screenshots, form interaction | Browser verification, visual checks, and web-app testing without leaving the agent loop |

## Candidates *(default)*

Evaluated positively - adoption awaits the trigger noted below.

| Server | Assessment | Adopt when |
|---|---|---|
| `codebase-memory-mcp` (MIT, local-only) | Redundant core with `codegraph` (same category: repo-wide symbol/call-graph indexing). Non-redundant edges: semantic vector code search, git-diff impact classification, ADR management tooling | Semantic code search, pre-push blast-radius checks, or ADR tooling become recurring needs; or working polyglot at monorepo scale beyond codegraph's language coverage |

## Rejected *(rule)*

Explicitly assessed and decided against - recorded with reasons so
decisions are never re-litigated casually. Re-evaluation happens only
when the rejection reasons change.

*(none recorded yet)*

## Rules

1. Servers are added only via documented harness configuration -
   never ad-hoc in a session.
2. Project-specific additions (e.g. a scoped playwright setup) are
   recorded in that project's README.
3. Unused or abandoned servers get removed at review time; the
   sanctioned table stays the single truth.
