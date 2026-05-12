# Review Findings

## 1. HIGH: No tests in previous package

Fix: Added pytest smoke tests for run-weekly, Telegram draft generation, and PPTX export.

## 2. HIGH: run-weekly could send Telegram immediately with flag but no dry-run safeguard

Fix: Added --dry-run and explicit send summary.

## 3. MEDIUM: Action extraction was too naive and often left owner/due date as TBD

Fix: Added lightweight owner and due-date extraction heuristics.

## 4. MEDIUM: No release notes

Fix: Added CHANGELOG.md.

## 5. MEDIUM: GitHub Actions only ran demo

Fix: Updated workflow to run pytest.

## 6. LOW: README was usable but not release-oriented

Fix: Rewrote README with upload-to-GitHub/Codex instructions.
