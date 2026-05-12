# Agent PMFlow MVP

**Agent PMFlow MVP** (`agent-pmflow-mvp`) is a minimal PM automation and Codex-ready agent project.

It turns a meeting transcript or notes file into:

- meeting protocol
- decision log
- action items
- weekly stakeholder status
- Telegram reminder draft
- Gantt/planning artifact
- PowerPoint outline and PPTX deck
- output manifest

The project is intentionally deterministic and small. The CLI command remains `pmflow`.

## Documentation

Detailed documentation:

- `docs/GETTING_STARTED.md`
- `docs/WORKFLOWS.md`
- `docs/REPORTING.md`
- `docs/ARTIFACT_FLOW.md`
- `docs/TELEGRAM.md`
- `docs/CODEX_USAGE.md`
- `docs/PROJECT_STRUCTURE.md`
- `docs/OPERATING_MODEL.md`
- `docs/PM_SKILLS.md`
- `docs/AGENT_COMPATIBILITY.md`

## Repository name

Recommended repository/package name:

```text
agent-pmflow-mvp
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
git commit -m "Initial Agent PMFlow MVP release"
gh repo create agent-pmflow-mvp --private --source=. --remote=origin --push
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
- does not add extra integrations

## Weekly workflow

The input artifact is a Markdown meeting note, transcript, or chat export. Put it here:

```text
meetings/inbox/product-sync.md
```

Run:

```bash
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

Generated files. See `docs/ARTIFACT_FLOW.md` for the full input and handoff contract:

```text
memory/meetings/product-sync-protocol.md
memory/decisions/product-sync-decisions.md
memory/actions/product-sync-actions.md
outputs/status/product-sync-weekly-status.md
outputs/telegram/product-sync-telegram-reminders.md
outputs/planning/product-sync-gantt.md
outputs/presentations/product-sync-outline.md
outputs/presentations/product-sync.pptx
outputs/product-sync-manifest.txt
```

## Product reports

Reporting is available as first-class CLI commands:

```bash
pmflow backlog-report --project-id campus-career-hub
pmflow roadmap-report --project-id campus-career-hub
pmflow executive-report --project-id campus-career-hub --title "Campus Career Hub"
```

Generated reports are written to `backlog/reports/`, `backlog/roadmap/`, and `outputs/reports/`. See `docs/REPORTING.md`.

## Safe Telegram mode

Draft only:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo
```

Dry-run send:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --send-telegram --dry-run
```

Real send only after explicit human request:

```bash
cp .env.example .env
# fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --send-telegram
```

## Gantt planning

Generated automatically by `run-weekly` as a Mermaid Markdown diagram. Only ISO due dates (`YYYY-MM-DD`) are placed on the timeline; vague dates stay in the PM review table.

Manual generation:

```bash
pmflow gantt --actions memory/actions/demo-actions.md --title demo
```

## PowerPoint

Generated automatically by `run-weekly`.

Skip PPTX:

```bash
pmflow run-weekly --meeting examples/demo-meeting.md --title demo --no-pptx
```


## Repository hygiene

Generated files are intentionally ignored by git:

- `*.egg-info/` from editable package installs
- `__pycache__/` and `*.pyc` from Python imports
- `.pytest_cache/` from pytest
- `memory/` and `outputs/` from local PMFlow runs

Use `.env.example` as the Telegram configuration template and keep real `.env` secrets local.

## What is intentionally excluded

- software development lifecycle automation
- Jira
- Confluence
- email automation
- RAG/vector DB
- multi-agent orchestration
- complex platform logic
- auto-escalation

Add extra integrations only when explicitly requested.
