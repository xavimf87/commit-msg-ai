---
layout: default
title: Usage
parent: Getting Started
nav_order: 5
---

# Usage

## Basic workflow

```bash
# 1. Make your changes
vim src/auth.py

# 2. Stage them
git add src/auth.py

# 3. Generate commit message
commitai
```

commitai will:

1. Read your staged diff (`git diff --staged`)
2. Show which files are staged
3. Send the diff to your local LLM
4. Display the proposed commit message
5. Ask for confirmation before committing

## Example output

```
Staged files:
M  src/auth.py
A  src/middleware.py

Generating commit message with qwen2.5-coder...

──────────────────────────────────────────────────
feat: add JWT authentication middleware
──────────────────────────────────────────────────

Commit with this message? [Y/n]
```

- Press **Enter** or **y** to commit
- Press **n** to abort

## Commit message format

All generated messages use one of three prefixes:

| Prefix | When to use |
|:-------|:------------|
| `feat:` | New features or functionality |
| `fix:` | Bug fixes |
| `bc:` | Breaking changes |

{: .note }
commitai never generates scoped prefixes like `feat(auth):`. Only clean `feat:`, `fix:`, or `bc:`.

## Using a different model

```bash
# Override for this run
commitai --model mistral

# Or change your default
commitai config model mistral
```

## No staged changes?

If you see:

```
No staged changes found. Stage your changes with `git add` first.
```

Make sure to run `git add` before `commitai`.
