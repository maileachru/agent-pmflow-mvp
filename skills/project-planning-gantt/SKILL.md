# Project Planning Gantt

## Purpose

Turn confirmed action items into a lightweight project plan and Mermaid Gantt diagram.

## Inputs

- `/memory/actions/<title>-actions.md`
- Action table with task, owner, due date, and status

## Outputs

- `/outputs/planning/<title>-gantt.md`

## Rules

- Use only existing action items.
- Do not invent tasks, owners, dependencies, or dates.
- Schedule only due dates that are explicit ISO dates: `YYYY-MM-DD`.
- Put natural-language dates such as `Friday`, `next week`, or `до пятницы` into `Unscheduled / Needs PM Review`.
- Keep the diagram Mermaid-compatible so it can be rendered by GitHub, many docs tools, or copied into other PM tooling.
- If no ISO dates exist, generate the file anyway and show a review-needed placeholder in the diagram.

## Minimal Workflow

```bash
pmflow gantt --actions memory/actions/<title>-actions.md --title <title>
```

The standard weekly workflow runs this automatically:

```bash
pmflow run-weekly --meeting meetings/inbox/<meeting>.md --title <title>
```
