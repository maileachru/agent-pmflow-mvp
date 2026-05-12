# Workflows

## Standard Weekly Workflow

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

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --send-telegram   --dry-run
```

---

## Real Telegram Send

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --send-telegram
```

---

## Skip PowerPoint

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync   --no-pptx
```
