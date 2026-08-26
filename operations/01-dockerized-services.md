---
title: Dockerized Services
type: reference
tags: [conventions, operations, docker]
status: accepted
created: 2026-08-25
updated: 2026-08-25
---

# Dockerized Services

One chapter per concern, all applying to every long-running container
on owned infrastructure - third-party images and self-built apps. The
edge provides TLS termination and single-sign-on; services stay behind
it.

## Compose conventions *(default)*

1. **One standalone stack per service**: `<stacks-root>/<service>/`
   containing its `docker-compose.yml` (+ `.env`). No shared
   mega-compose; related containers of one service live in that stack.
2. The stack is deployed from infrastructure-as-code as the reproducible
   baseline; console changes are day-2 operations and get promoted back
   into the code.
3. Image tags: track a pinned major line (`image:13`) or `latest` where
   update-watch tooling should see freshness; digests for release-critical
   images.
4. `restart: unless-stopped` on every service. Subtlety, on purpose: a
   manual stop survives host reboots - use `start`, not just reboot,
   after intentional downtime.
5. Resource bounds (`mem_limit`, `cpus`) set per service so one stack
   cannot starve the rest.

## Third-party images *(default)*

Consumed unmodified: configuration happens through env, volumes, and
command only - no local forks or patched copies without a documented
decision. Adoption is deliberate: project/source vetted, major tag
pinned.

Because we adapt every stack to our routing anyway, upstream sample
compose files are never used as-is - and hardening is applied
regardless of what the vendor ships:

```yaml
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    # cap_add: only the single capabilities the image documents as needed
```

- `privileged: true` and `network_mode: host` are justified exceptions,
  each documented next to the stack.
- Read-only root filesystems plus tmpfs mounts wherever the image
  tolerates it.

## Routing & authentication *(default)*

1. Every browser-facing UI/API gets a hostname route on the edge
   reverse proxy; TLS terminates there, never in the service.
2. Single-sign-on forward-auth is attached **by default**. Public
   routes are explicit, documented exceptions with their own protection
   (token, JWT, mTLS).
3. Admin surfaces restrict to an admin group or admin network.
4. Services must be reverse-proxy-ready: trust proxy headers, generate
   correct external URLs, keep relative paths where possible.

## Users & permissions *(rule)*

1. Containers run as **non-root** unless the image makes it impossible;
   every exception is documented next to the stack.
2. Host mounts are read-only wherever possible.
3. The docker socket is never mounted into application containers; a
   least-privilege socket proxy is the only approved path when
   control APIs are needed.

## Networking *(default)*

1. Services join the shared proxy network only when they expose a UI or
   API to the edge; databases and backends sit on isolated internal
   networks.
2. No published host ports unless a non-container client genuinely
   needs them - service-to-service traffic uses network aliases.
3. Sensitive egress (scraping, automation) routes through dedicated
   gateway containers on segmented networks.

## State & secrets *(default)*

1. Persistent data in named volumes or bind mounts under the defined
   data root - never inside the container layer, never lost on rebuild.
2. Secrets via `.env` (gitignored, example committed) or mounted secret
   files; nothing sensitive baked into images or compose files.
3. Every stack documents what in its state must be backed up, and how
   often.

## Logging *(default)*

1. Containers write logs to **stdout/stderr** - collected by the docker
   daemon and readable via `docker logs`. No log files inside volumes.
2. Line format follows [`../development/13-logging.md`](../development/13-logging.md):
   ISO timestamp with offset, level, filterable identifiers.
3. Rotation is bounded per service through the daemon driver:

```yaml
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## Lifecycle *(default)*

1. Each service defines a `healthcheck`; dependent stacks use it.
2. Updates are watch-detected and manually applied through the ops UI;
   major-version bumps get a compatibility check first.
3. Deprecating a service means removing its stack, route, auth entry,
   and state in one cleanup change.
