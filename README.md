# PMFlow Codex

**PMFlow Codex** is a minimal Project Manager operating system for Codex.

It turns a meeting transcript or notes file into:

- meeting protocol
- decision log
- action items
- weekly stakeholder status
- Telegram reminder draft
- PowerPoint deck
- output manifest



## Documentation

Detailed documentation:

- `docs/GETTING_STARTED.md`
- `docs/WORKFLOWS.md`
- `docs/TELEGRAM.md`
- `docs/CODEX_USAGE.md`
- `docs/PROJECT_STRUCTURE.md`
- `docs/OPERATING_MODEL.md`

## Repository name

Recommended name:

```text
pmflow-codex
```

## Main command

```bash
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pmflow doctor
pmflow demo
pytest
```

## Upload to GitHub

```bash
git init
git add .
git commit -m "Initial PMFlow Codex release"
gh repo create pmflow-codex --private --source=. --remote=origin --push
```

Then connect the GitHub repository in Codex.

## Codex check

```bash
codex "$(cat scripts/codex-test-prompt.md)"
```

Expected behavior:

- reads `AGENTS.md`
- uses `pmflow run-weekly`
- creates PM artifacts
- does not send Telegram messages

## Weekly workflow

Put meeting notes here:

```text
meetings/inbox/product-sync.md
```

Run:

```bash
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

Generated files:

```text
memory/meetings/product-sync-protocol.md
memory/decisions/product-sync-decisions.md
memory/actions/product-sync-actions.md
outputs/status/product-sync-weekly-status.md
outputs/telegram/product-sync-telegram-reminders.md
outputs/presentations/product-sync-outline.md
outputs/presentations/product-sync.pptx
outputs/product-sync-manifest.txt
```

## Safe Telegram mode

Draft only:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo
```

Dry-run send:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --send-telegram --dry-run
```

Real send:

```bash
cp .env.example .env
# fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --send-telegram
```

## PowerPoint

Generated automatically by `run-weekly`.

Skip PPTX:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --no-pptx
```

## What is intentionally excluded

- Jira
- Confluence
- email automation
- RAG/vector DB
- multi-agent orchestration
- auto-escalation

These should be added only after the first workflow is used in real PM operations.
