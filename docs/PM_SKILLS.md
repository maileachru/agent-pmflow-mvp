# PM Skill Library

Agent PMFlow MVP is a small skill-based project manager assistant. It is designed for PM artifacts, not software development automation.

## Active Skills

| Skill | Folder | Primary artifact | When to use |
|---|---|---|---|
| Meeting protocol generation | `skills/meeting-protocol-generation/` | protocol, decisions, actions | After a meeting or transcript arrives |
| Stakeholder status reporting | `skills/stakeholder-status-reporting/` | weekly status | For weekly stakeholder updates |
| Project planning Gantt | `skills/project-planning-gantt/` | Mermaid Gantt plan | When action items need a timeline |
| Presentation generation | `skills/presentation-generation/` | outline and PPTX | For executive/project update decks |

## Skill Design Rules

Every PM skill should stay:

- **Deterministic** — same input produces the same artifact shape.
- **Small** — one skill owns one PM job.
- **Reviewable** — generated artifacts are Markdown-first and easy to edit.
- **Human-approved** — external communication is drafted by default and sent only after explicit approval.

## Standard Weekly Skill Chain

```text
meeting notes
  ↓
meeting-protocol-generation
  ↓
decisions + action items
  ↓
stakeholder-status-reporting
  ↓
project-planning-gantt
  ↓
presentation-generation
  ↓
Telegram draft only
```

Run it with:

```bash
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

## Adding a New PM Skill

Add a new skill only when the workflow is a real PM need and cannot be handled by the existing artifacts.

Minimum required files:

```text
skills/<skill-name>/SKILL.md
templates/<artifact-template>.md
```

The `SKILL.md` should define:

1. Purpose
2. Inputs
3. Outputs
4. Rules
5. Minimal command or workflow

## Out of Scope

Do not add engineering lifecycle automation, Jira, Confluence, email automation, RAG, vector databases, risk engines, or multi-agent orchestration unless a human explicitly asks for it.
