# PMFlow Codex — Agent Instructions

This repository is a deterministic PM automation system for Codex.

## Primary Workflow

Use this command for the standard weekly workflow:

```bash
pmflow run-weekly --meeting <meeting-file> --title <title>
```

## Core Rule

Do not invent process. Use the smallest relevant workflow.

## Active Capabilities

Only these capabilities are active:

1. Meeting protocol generation
2. Decision extraction
3. Action item extraction
4. Weekly stakeholder status
5. Telegram reminder draft
6. Optional Telegram send
7. PowerPoint outline and PPTX export

Everything else is intentionally out of scope.

## Required Skill Loading

For every PM task:

1. Read this file.
2. Identify the PM task.
3. Read only the required `skills/<skill>/SKILL.md`.
4. Use templates from `/templates`.
5. Save artifacts into the required output folders.

## Folder Contracts

- Incoming notes/transcripts: `/meetings/inbox`
- Meeting protocols: `/memory/meetings`
- Decisions: `/memory/decisions`
- Action items: `/memory/actions`
- Weekly status reports: `/outputs/status`
- Telegram messages: `/outputs/telegram`
- Presentation outlines and PPTX files: `/outputs/presentations`

## Human Review Rule

Never send Telegram messages unless the user explicitly asks to send.

Default behavior:
- Generate Telegram draft only.

Sending is allowed only when the user explicitly says:
- send
- отправь
- publish
- notify

When testing Telegram sending, use:

```bash
pmflow run-weekly --meeting <meeting-file> --title <title> --send-telegram --dry-run
```

## Minimalism Rule

Do not add Jira, Confluence, email, RAG, vector database, risk engine, or multi-agent orchestration unless explicitly requested.
