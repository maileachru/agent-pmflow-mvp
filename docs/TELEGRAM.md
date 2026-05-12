# Telegram Setup

Agent PMFlow MVP generates Telegram reminder drafts by default.

Never send Telegram messages unless the user explicitly requests sending.

## 1. Create bot

Open BotFather:

https://t.me/BotFather

Create bot and get token.

---

## 2. Create .env

```bash
cp .env.example .env
```

Add:

```env
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
```

---

## 3. Test direct send only when explicitly requested

```bash
pmflow telegram-send --message "test"
```

---

## 4. Production Rule

Default workflow should generate drafts only.

Only send messages after explicit human review and approval.
