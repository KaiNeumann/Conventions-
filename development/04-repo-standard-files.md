---
title: Repo Standard Files
type: reference
tags: [conventions, development, standards]
status: accepted
created: 2026-08-23
updated: 2026-08-25
---

# Repo Standard Files

New repos start with these files, copied from here — contents below are
**default templates**, adapt per project. The only hard rules: a repo is
never pushed without a `.gitignore` that covers its generated artifacts,
and real secrets/`.env` never enter git (see
[`01-git.md`](01-git.md)).

## Temporary artifacts *(rule)*

1. Development artifacts, evidence, and throwaway files — test output,
   screenshots, API dumps, scratch scripts, downloaded samples — are
   **never written into the user's home directory** (`~`,
   `%USERPROFILE%`, Desktop, Documents).
2. They live exclusively in **`temp/`** at the project root. The
   directory is always gitignored (see baseline below), always
   disposable, and safe to delete at any time.
3. **Clean `temp/` frequently.** Anything worth keeping moves to its
   proper home (a test, an example, documentation) or is deleted —
   `temp/` must never turn into a second project.
4. Persistent application state follows [`15-settings.md`](15-settings.md)
   (sidecar/profile); only disposable junk goes into `temp/`.
5. Agents: never write scratch files outside the project; when working
   without a project context, ask where to put them.

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

Web block, when the repo has a frontend:

```editorconfig
[*.js]
[*.ts]
[*.json]
[*.yml]
indent_style = space
indent_size = 2
```

## `.gitattributes`

Closes the LF-enforcement gap: `.editorconfig` guides editors only —
this file makes git itself normalize line endings (see the
[`01-git.md`](01-git.md) cross-platform rule).

```gitattributes
* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.db binary
*.sqlite binary
```

## `.gitignore` (Python app baseline)

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# Tooling / agent state
temp/
.sisyphus/
.playwright-mcp/
.codegraph/
.pytest_cache/
.ruff_cache/

# Build output (any ecosystem)
build/
dist/

# Frontend deps
node_modules/

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
build
dist
temp
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

## `LICENSE`

Every repo declares its license explicitly — pick from the decision
table in [`15-licensing.md`](15-licensing.md) and SPDX-declare in
`pyproject.toml` / `package.json` when those manifests exist.

## `AGENTS.md` / `README.md`

Required content defined in [`06-documentation.md`](06-documentation.md);
CI-enabled repos additionally carry the automation contract there
([`12-task-automation.md`](12-task-automation.md)).

## Rule of origin

These files are copied from this conventions repo when a project starts.
Improvements get made here first, then propagated — not the other way
around.
