# Changelog

## 0.4.0

### Added

- Added deterministic Mermaid Gantt planning output from action items.
- Added a project-planning Gantt skill and template.
- Added PM skill-library and multi-agent compatibility documentation for Codex, Claude Code, Cursor, Gemini CLI, Windsurf, OpenCode, GitHub Copilot, Kiro, and other agents.

### Changed

- Updated the standard weekly workflow documentation to include the planning artifact while keeping Telegram send human-approved.

## 0.3.2

### Changed

- Renamed repository/package branding to Agent PMFlow MVP (`agent-pmflow-mvp`).
- Kept the CLI command as `pmflow`.
- Updated package metadata to describe the project as PM automation and Codex-ready.
- Updated README, AGENTS.md, and docs to reinforce deterministic minimalism, `pmflow run-weekly`, and Telegram human-review rules.

### Removed

- Removed generated Python package/cache artifacts from the repository tree.

## 0.3.0

### Added

- Safer and more complete `run-weekly` workflow.
- `--dry-run` mode.
- `--no-pptx` option.
- `--telegram-message-limit` protection.
- Basic pytest test suite.
- `REVIEW.md` with review findings.
- Better action item parsing with simple owner/due-date extraction.
- Better output manifest.
- Safer Telegram sending rules.

### Changed

- Package version bumped to `0.3.0`.
- CLI output is now more explicit.
- README updated for Codex/GitHub upload.
- GitHub Actions now runs tests.

### Fixed

- Generated Telegram reminder file names were too verbose.
- `weekly-status` output naming could duplicate suffixes.
- `run-weekly` lacked dry-run support.
- Demo workflow did not validate produced artifacts.
