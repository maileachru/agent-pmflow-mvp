# Workflows

## Standard Weekly Workflow

Input: one Markdown meeting note, transcript, or chat export in `meetings/inbox/`. Use `pmflow run-weekly` as the primary Agent PMFlow MVP workflow:

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync
```

Generates the full artifact chain documented in `docs/ARTIFACT_FLOW.md`:

- meeting protocol
- decision log
- action items
- weekly status
- Telegram reminder draft
- Mermaid Gantt plan
- PowerPoint deck

---

## Safe Telegram Test

Use dry-run mode for send testing:

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --send-telegram   --dry-run
```

---

## Real Telegram Send

Run only when the user explicitly requests sending:

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --send-telegram
```

---

## Generate Gantt Only

Input: the action table generated at `memory/actions/<title>-actions.md`.

```bash
pmflow gantt --actions memory/actions/product-sync-actions.md --title product-sync
```

Gantt generation schedules only explicit ISO due dates (`YYYY-MM-DD`) and keeps vague dates in a PM review table.

---

## Skip PowerPoint

Use this when the Markdown outline is enough and no PPTX file is needed.

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --no-pptx
```
