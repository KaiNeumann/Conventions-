---
title: Operations
type: reference
tags: [conventions, operations]
status: accepted
created: 2026-08-25
updated: 2026-08-25
---

# Operations

Standards for running containerized services on owned infrastructure -
third-party images and self-built applications alike.

**Boundary:** build-time rules live in
[`../development/`](../development/README.md) (packaging, Dockerfile,
health endpoints); infrastructure-specific implementation details live
with the infrastructure repository. This area defines what always
applies, independent of any concrete host or domain.

Chapters are tiered like everywhere else
([`../README.md`](../README.md)): rule / default / pattern.

## Chapters

1. [`01-dockerized-services.md`](01-dockerized-services.md) - compose,
   routing/auth, users, networking, lifecycle for every long-running
   service
