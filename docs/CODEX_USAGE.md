# Codex Usage

Agent PMFlow MVP is a Codex-ready PM automation agent project.

## Open project

```bash
codex
```

## Recommended Prompt

```text
Read AGENTS.md.

Run weekly workflow for:
meetings/inbox/product-sync.md

Generate:
- protocol
- decisions
- action items
- weekly status
- Telegram reminders
- PowerPoint deck

Do not send Telegram messages.
Do not add extra integrations.
```

---

## What Codex Should Do

Codex should:

1. Read `AGENTS.md`
2. Load required skills
3. Use `pmflow run-weekly`
4. Save artifacts into correct folders
5. Avoid adding extra frameworks or integrations
6. Keep the workflow deterministic and minimal
