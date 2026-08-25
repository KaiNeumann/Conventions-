---
title: Packaging — Dockerized Web Apps
type: reference
tags: [conventions, development, docker]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Packaging — Dockerized Web Apps

Default delivery mode for anything multi-user or server-bound. One part
of the "one core, many shells" model — siblings:
[`09-packaging-desktop.md`](09-packaging-desktop.md),
[`10-cross-platform.md`](10-cross-platform.md),
[`11-releases.md`](11-releases.md).

## Dockerized web app (default, with inline rules)

Applies when a project ships as a Dockerized web app.

1. *(default)* Base image: official slim (`python:3.12-slim`); pin digest
   for release images.
2. *(rule)* Final image runs as **non-root user**.
3. *(rule)* State in **named volumes** (`rss-data`, `pg-data`) or
   bind-mounted `data/` — never inside the container layer.
4. *(default)* Every service exposes `/healthz`; compose has healthchecks.
5. *(default)* `docker-compose.yml` is the deployment unit; long-lived
   settings via mounted config files, secrets via `secrets/` mount or
   `.env` (gitignored, `.env.example` committed).
6. *(default)* Ports stay on internal networks; TLS + auth terminate at
   the edge reverse proxy / auth service. Apps must
   be reverse-proxy-ready (trust proxy headers, relative URLs where sane).
7. *(rule)* Network segmentation for sensitive flows: isolated
   internal networks, exactly one dual-homed gateway service; no
   blanket external egress.
8. *(default)* Public images tag `latest` (WUD-friendly); pinned tags
   need a documented exception.

## Build gating

*(default)* Per-push CI runs tests only. Docker image builds and
publishes happen on `v*` tags or manual dispatch — never in the
per-push hot path ([`12-task-automation.md`](12-task-automation.md),
Open decisions #1).
