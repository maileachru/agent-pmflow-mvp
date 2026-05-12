# Agent PMFlow MVP — Agent Instructions

This repository is a deterministic, minimal PM automation system for Codex.

## Primary Workflow

Use this command for the standard weekly workflow:

```bash
pmflow run-weekly --meeting <meeting-file> --title <title>
```

Keep the CLI command name as `pmflow`.

## Core Rule

Do not invent process. Use the smallest relevant workflow and keep the system deterministic and minimal.

## Active Capabilities

Only these capabilities are active:

1. Meeting protocol generation
2. Decision extraction
3. Action item extraction
4. Weekly stakeholder status
5. Telegram reminder draft
6. Optional Telegram send
7. Project planning Gantt diagram
8. PowerPoint outline and PPTX export

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
- Gantt planning diagrams: `/outputs/planning`

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

Do not add extra integrations unless explicitly requested.

Do not add Jira, Confluence, email automation, RAG, vector database, risk engine, multi-agent orchestration, or complex platform logic unless explicitly requested.
