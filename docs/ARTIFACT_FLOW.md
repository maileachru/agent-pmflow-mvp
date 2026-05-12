# Artifact Flow and Input Contracts

This document is the operational map for what to give PMFlow as input, what it produces, and how a PM or agent should move through the workflow.

## Default path

Use the standard weekly workflow unless the user asks for a narrower artifact:

```bash
pmflow run-weekly --meeting meetings/inbox/<meeting-file>.md --title <title>
```

The workflow is intentionally linear:

```text
meetings/inbox/<meeting-file>.md
  -> memory/meetings/<title>-protocol.md
  -> memory/decisions/<title>-decisions.md
  -> memory/actions/<title>-actions.md
  -> outputs/status/<title>-weekly-status.md
  -> outputs/telegram/<title>-telegram-reminders.md
  -> outputs/planning/<title>-gantt.md
  -> outputs/presentations/<title>-outline.md
  -> outputs/presentations/<title>.pptx
  -> outputs/<title>-manifest.txt
```

## Primary input artifact

The only required input for `run-weekly` is a Markdown meeting note, transcript, or chat export file.

Place it in:

```text
meetings/inbox/
```

Recommended shape:

```markdown
# Product Sync

Date: 2026-05-12
Project: Short project context.

## Attendees
- Anna — PM
- Boris — Engineering Lead

## Notes
Decision: We will run a limited pilot first.
Anna will publish the pilot charter by 2026-05-13.
Boris will prepare the prototype by 2026-05-22.
Risk: Data export may be delayed.
Open question: Should partners see confidence scores?

## Meetings planned
- Pilot readiness review: 2026-05-29.
```

## Extraction cues

PMFlow is deterministic and does not infer missing PM data. Use explicit cues in the source notes when possible.

| Artifact generated | Source cue to put in meeting notes | Result |
|---|---|---|
| Decisions | `Decision:` or `Решение:` | Added to `memory/decisions/<title>-decisions.md` |
| Risks / blockers | `Risk:`, `Риск:`, `blocker`, `blocked`, `блокер` | Added to protocol risks and presentation risks |
| Open questions | `Open question:`, `Вопрос:`, `should`, `нужно ли` | Added to protocol open questions |
| English actions | `<Owner> will <task> by <due>` or `<Owner> review <task> by <due>` | Added to action table |
| Russian actions | `<Owner> должен <task> до <due>`, `<Owner> подготовит <task> до <due>`, or `<Owner> сделает <task> до <due>` | Added to action table |

If an owner or due date is not explicit in a matched action pattern, PMFlow uses `TBD`. If a line is not an explicit action, it should remain context rather than being forced into the action table.

## Date handling

Use ISO due dates (`YYYY-MM-DD`) for action items that should appear on the Mermaid Gantt timeline.

Examples:

```markdown
Anna will publish the charter by 2026-05-13.
Boris will prepare the prototype by 2026-05-22.
```

Natural-language dates are allowed, but they are not scheduled on the Gantt timeline:

```markdown
Anna will schedule the readiness review by Friday.
Elena will prepare support macro examples by next week.
```

Those items stay in `Unscheduled / Needs PM Review` until a PM confirms an ISO date.

## Generated artifacts and next step

| Step | Artifact | Produced by | Next consumer / action |
|---|---|---|---|
| 1 | `memory/meetings/<title>-protocol.md` | `process-meeting` inside `run-weekly` | PM reviews context, decisions, actions, risks, open questions |
| 2 | `memory/decisions/<title>-decisions.md` | `process-meeting` inside `run-weekly` | Used by weekly status and presentation outline |
| 3 | `memory/actions/<title>-actions.md` | `process-meeting` inside `run-weekly` | Used by weekly status, Telegram draft, and Gantt generation |
| 4 | `outputs/status/<title>-weekly-status.md` | `weekly-status` inside `run-weekly` | PM edits/sends as stakeholder status if appropriate |
| 5 | `outputs/telegram/<title>-telegram-reminders.md` | `telegram-reminders` inside `run-weekly` | PM reviews; do not send without explicit approval |
| 6 | `outputs/planning/<title>-gantt.md` | `gantt` inside `run-weekly` | PM reviews scheduled vs unscheduled actions |
| 7 | `outputs/presentations/<title>-outline.md` | `process-meeting` inside `run-weekly` | Source for PPTX export and PM editing |
| 8 | `outputs/presentations/<title>.pptx` | `pptx` inside `run-weekly` | Stakeholder deck after PM review |
| 9 | `outputs/<title>-manifest.txt` | `run-weekly` | Checklist of generated artifact paths |

## Human review gates

Before communicating externally, a PM should review:

1. `memory/actions/<title>-actions.md` for false positives, missing owners, and missing ISO dates.
2. `memory/decisions/<title>-decisions.md` for decision wording and missing rationale/owner.
3. `outputs/status/<title>-weekly-status.md` for stakeholder tone.
4. `outputs/telegram/<title>-telegram-reminders.md` before any send.
5. `outputs/planning/<title>-gantt.md` for unscheduled items that need PM date confirmation.
6. `outputs/presentations/<title>-outline.md` and the PPTX before presentation use.

Telegram must remain draft-only unless the user explicitly says to send, отправь, publish, or notify.

## Manual artifact commands

Use these only when you need one artifact instead of the full weekly workflow.

| Need | Input artifact | Command |
|---|---|---|
| Protocol, decisions, actions, outline | `meetings/inbox/<meeting>.md` | `pmflow process-meeting meetings/inbox/<meeting>.md --title <title>` |
| Weekly status only | `memory/actions/<title>-actions.md` and optionally `memory/decisions/<title>-decisions.md` | `pmflow weekly-status --title <title> --actions memory/actions/<title>-actions.md --decisions memory/decisions/<title>-decisions.md` |
| Telegram draft only | `memory/actions/<title>-actions.md` | `pmflow telegram-reminders --actions memory/actions/<title>-actions.md` |
| Gantt only | `memory/actions/<title>-actions.md` | `pmflow gantt --actions memory/actions/<title>-actions.md --title <title>` |
| PPTX only | `outputs/presentations/<title>-outline.md` | `pmflow pptx --outline outputs/presentations/<title>-outline.md --output outputs/presentations/<title>.pptx` |
| Telegram send | Reviewed message text | `pmflow telegram-send --message "..." --dry-run` for tests; remove `--dry-run` only after explicit approval |

## What not to provide as input

Do not provide Jira exports, Confluence pages, email threads, vector databases, or integration payloads unless a human explicitly asks to extend the project. For the MVP, convert relevant information into a concise Markdown meeting note under `meetings/inbox/` and run the standard workflow.
