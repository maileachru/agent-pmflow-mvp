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

## Skip PowerPoint

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --no-pptx
```
