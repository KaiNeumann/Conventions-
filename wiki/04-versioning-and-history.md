---
title: Versioning and History
type: reference
tags: [conventions, wiki, git]
status: accepted
created: 2026-08-23
updated: 2026-08-24
---

# Versioning and History

Applies to vaults that are git-versioned (the default). Git history is the
changelog — do not maintain a parallel one.

## History discipline (rule)

1. **Git history is the changelog.** Notes keep no manual "Changelog"
   sections for routine edits. Exceptions: decisions and specs may log
   status transitions via frontmatter (`status` + `updated`).
2. **Bump `updated`** on substantive edits; never touch `created`.
3. Conflicts: rebase locally before pushing; when resolving, content
   correctness wins over either side's wording. When unsure which version
   is right — ask the human, don't merge blind.

## Commit habits (default)

1. One logical change per commit; messages per
   [`../development/01-git.md`](../development/01-git.md).
2. Small frequent syncs: commit and push after each working session;
   long-lived local divergence is how conflicts happen.
3. **Lean bundled assets**: compress images before committing
   (screenshots rarely need full resolution); megabyte-scale media
   (video, huge scans) lives outside the vault and gets linked from the
   bundle instead. Keeps clone/push fast without breaking
   self-containment for ordinary notes.

## Deprecation instead of deletion (rule)

1. Agents **MUST NOT** delete content without explicit instruction;
   flag it instead (see
   [`05-human-agent-collaboration.md`](05-human-agent-collaboration.md)).
2. Outdated notes get `status: deprecated` plus a link to the replacement,
   deleted once the replacement is accepted.
3. Truly wrong/dangerous content (secrets, wrong safety info) is removed
   immediately, not deprecated — deletion with human sign-off.
