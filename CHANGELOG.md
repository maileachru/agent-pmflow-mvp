# Changelog

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
