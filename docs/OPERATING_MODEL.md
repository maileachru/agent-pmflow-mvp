# Operating Model

Agent PMFlow MVP is not an AI chat assistant.

It is a deterministic PM automation workflow for Codex-ready meeting follow-up.

## Principle

```text
Meeting
  ↓
Transcript
  ↓
pmflow run-weekly
  ↓
Protocol
Actions
Status
Telegram draft
PPTX
```

## Human Responsibilities

Human PM remains responsible for:

- decisions
- approvals
- communication
- prioritization
- explicitly approving any Telegram send

## System Responsibilities

Agent PMFlow MVP automates:

- formatting
- extraction
- reporting
- reminder draft generation
- presentation generation

## What NOT to do

Do not turn the project into:

- AI platform
- agent swarm
- enterprise orchestration layer
- giant integration hub
- Jira, Confluence, email, RAG, or vector database system

Keep the workflow small, deterministic, and reliable.
