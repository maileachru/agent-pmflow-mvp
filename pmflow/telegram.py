from __future__ import annotations

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from .utils import write_text, slugify, markdown_table_rows


def generate_reminders(actions_path: str, message_limit: int = 20) -> str:
    lines: list[str] = []
    rows = markdown_table_rows(actions_path)

    for parts in rows[:message_limit]:
        if len(parts) >= 4:
            task, owner, due_date, status = parts[:4]
            if task and task != "TBD":
                lines.append(f"Reminder: {task}\nOwner: {owner}\nDue: {due_date}\nStatus: {status}")

    if len(rows) > message_limit:
        lines.append(f"Note: {len(rows) - message_limit} more action item(s) omitted by message limit.")

    message = "\n\n---\n\n".join(lines) if lines else "No actionable reminders found."

    stem = Path(actions_path).stem
    stem = stem.removesuffix("-actions")
    output = f"outputs/telegram/{slugify(stem)}-telegram-reminders.md"
    return write_text(output, message)


def send_message(message: str, dry_run: bool = False) -> dict:
    if dry_run:
        return {"ok": True, "dry_run": True, "message": message}

    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=30)
    response.raise_for_status()
    return response.json()


def send_file_text(path: str, dry_run: bool = False) -> dict:
    message = Path(path).read_text(encoding="utf-8")
    return send_message(message, dry_run=dry_run)
