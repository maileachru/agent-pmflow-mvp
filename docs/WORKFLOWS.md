# Workflows

## Standard Weekly Workflow

Use `pmflow run-weekly` as the primary Agent PMFlow MVP workflow:

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync
```

Generates:

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

```bash
pmflow gantt --actions memory/actions/product-sync-actions.md --title product-sync
```

Gantt generation schedules only explicit ISO due dates (`YYYY-MM-DD`) and keeps vague dates in a PM review table.

---

## Skip PowerPoint

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --no-pptx
```
