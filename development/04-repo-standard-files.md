---
title: Repo Standard Files
type: reference
tags: [conventions, development, standards]
status: draft
created: 2026-08-23
updated: 2026-08-23
---

# Repo Standard Files

New repos start with these files, copied from here — contents below are
**default templates**, adapt per project. The only hard rules: a repo is
never pushed without a `.gitignore` that covers its generated artifacts,
and real secrets/`.env` never enter git (see
[`01-git.md`](01-git.md)).

## `.editorconfig`

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4

[*.ps1]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

(MD keeps trailing whitespace: two spaces are hard line breaks.)

## `.gitignore` (Python app baseline)

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# Tooling / agent state
.tmp/
.sisyphus/
.playwright-mcp/
.pytest_cache/
.ruff_cache/

# Node (when frontend present)
node_modules/
dist/

# Runtime data & secrets
data/
logs/
*.db
*.sqlite
.env
secrets/
```

Add per-project entries on top; delete what does not apply.

## `.dockerignore`

```dockerignore
.git
.codegraph
.omo
.sisyphus
.venv
__pycache__
*.db
*.sqlite
data/
logs/
Dockerfile
docker-compose.yml
.dockerignore
```

Build context stays minimal — smaller builds, no secret leakage into
layers.

## `.env.example` (when env config is used)

Committed example with every variable and a placeholder value:

```dotenv
DB_PASSWORD=changeme
TOR_PROXY=socks5h://127.0.0.1:9050
```

Real `.env` and `secrets/` are gitignored, always.

## `AGENTS.md` / `README.md`

Required content defined in [`06-documentation.md`](06-documentation.md).

## Rule of origin

These files are copied from this conventions repo when a project starts.
Improvements get made here first, then propagated — not the other way
around.
