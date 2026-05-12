# Repository Review

## Current Production Assessment

Agent PMFlow MVP is correctly scoped as a minimal, deterministic PM automation agent:

- Primary workflow is `pmflow run-weekly`.
- CLI command remains `pmflow`.
- Core outputs are meeting protocol, decisions, action items, weekly status, Telegram draft, and PowerPoint deck.
- Telegram sending is opt-in and should happen only after explicit human approval.
- Jira, Confluence, email automation, RAG, vector databases, and multi-agent orchestration remain out of scope.

## Why generated files are not kept in git

The following files/directories are generated locally and should not be versioned:

- `*.egg-info/` — Python packaging metadata produced by `pip install -e .`.
- `__pycache__/` and `*.pyc` — Python bytecode caches produced when modules are imported.
- `.pytest_cache/` — pytest runtime cache.
- `memory/` and `outputs/` — PMFlow artifacts produced by demo and weekly workflow runs.

Keeping them out of git makes diffs smaller, avoids machine-specific noise, and prevents stale package metadata after renames.

## Changes made from this review

- Added `.gitignore` for Python caches, package build artifacts, local environments, secrets, and generated PMFlow outputs.
- Added `.env.example` because Telegram documentation references it.

## Recommendations

### Keep now

- Keep `pmflow run-weekly` as the main workflow.
- Keep direct subcommands only as small utilities for debugging or manual artifact generation.
- Keep Telegram real sending behind explicit human approval.
- Keep generated files out of the repository unless they are curated examples.

### Improve next, still minimal

1. Add one CLI smoke test for `pmflow doctor`.
2. Add one test that confirms `run_weekly(..., send_telegram=False)` never calls Telegram sending.
3. Add a tiny sample expected-output fixture only if human reviewers need a stable artifact example.
4. Consider validating that `--send-telegram` without `--dry-run` requires environment variables before workflow work begins, so failures happen early.

### Do not add unless explicitly requested

- Jira, Confluence, email automation, RAG, vector database, risk engine, multi-agent orchestration, or complex platform logic.
