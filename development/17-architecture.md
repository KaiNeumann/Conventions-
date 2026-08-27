---
title: Architecture and Data Pipelines
type: reference
tags: [conventions, development, architecture, pipelines]
status: accepted
created: 2026-08-27
updated: 2026-08-27
---

# Architecture and Data Pipelines

Build replaceable systems without pre-building a platform. Keep source data
and application logic independent of providers, agents, and derived stores.

## Integration boundaries *(default)*

1. Third-party services and utilities sit behind a local interface. The
   application core depends on that interface, not directly on a model,
   storage provider, downloader, or external API client.
2. Define an interface when replacement is foreseeable, but implement one
   backend until another is needed. SQLite before a server database, a simple
   worker before a distributed queue, and one model before a model router.
3. Provider adapters share conformance tests when replacement would affect
   behavior. The tests define the local contract, not a provider's incidental
   response shape.

## Processing pipelines *(default)*

1. A user-facing request enqueues long-running downloads, OCR, transcoding,
   indexing, and enrichment work instead of waiting for it. Jobs record state,
   attempts, timestamps, errors, and enough input to resume safely.
2. Operations are idempotent where practical. Use stable identifiers, content
   hashes, uniqueness constraints, and explicit processing states so a retry
   does not duplicate results.
3. Acquisition stores the original before enrichment. OCR, extracted text,
   normalized records, thumbnails, embeddings, and similar outputs are
   derivatives that can be regenerated without reacquiring the source.
4. Persist provenance with generated or extracted results: source location,
   acquisition time, extractor or model version, and validation outcome.

## Contracts and formats *(rule)*

1. Pipeline stages exchange defined schemas, never arbitrary prose. Parse and
   validate input and output at every boundary; reject or repair invalid data
   before the next stage consumes it.
2. Prefer simple, documented, open, text-based formats at boundaries:
   Markdown for prose, CSV for flat tables, JSON for structured interchange,
   YAML for human-maintained configuration, and plain text where structure is
   unnecessary. Choose the smallest format that preserves the needed meaning.
3. Canonical data is human-readable and independent of derived indexes.
   Search indexes, embeddings, caches, and generated summaries are disposable
   and rebuildable from their authoritative sources.
4. Token-Oriented Object Notation (TOON) is allowed as a lossless,
   JSON-shaped translation layer for structured LLM context. Use it only when
   its compact tabular form benefits sufficiently uniform data and token cost
   matters. JSON remains the default programmatic and API format; CSV remains
   preferable for purely flat tables. Do not make TOON the sole canonical
   store or an API contract without a documented need.

## AI boundaries *(default)*

1. Route by explicit task type, sensitivity, token budget, context size, and
   provider capability before asking a model to choose a route.
2. Improve retrieval, compact tool output, structured state, and prompt scope
   before selecting a larger or more expensive model.
3. Extraction and classification represent unknown and ambiguous values
   explicitly, with a reason or validation error, rather than inventing a
   value.
4. Redaction, provider policy, approval checks, and capability restrictions
   belong at a shared boundary when multiple agents or applications use them.
   That boundary enforces policy but does not absorb domain capabilities.
