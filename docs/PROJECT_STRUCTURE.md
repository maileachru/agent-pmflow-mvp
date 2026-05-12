# Project Structure

```text
agent-pmflow-mvp/
│
├── AGENTS.md
├── README.md
├── docs/
├── examples/
├── integrations/
├── meetings/
├── memory/
├── outputs/
├── pmflow/
├── skills/
├── templates/
└── tests/
```

## Main Folders

### meetings/inbox

Incoming meeting transcripts or notes.

### memory

Persistent PM artifacts:

- protocols
- decisions
- actions

### outputs

Generated operational outputs:

- status reports
- Telegram drafts
- PPTX files

### pmflow

Python package that exposes the `pmflow` CLI.

### skills

Deterministic PM skills used by Codex.

### templates

Markdown templates for generated artifacts.
