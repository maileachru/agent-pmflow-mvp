from __future__ import annotations

from pathlib import Path

from pmflow.telegram import generate_reminders, send_message


def test_generate_reminders(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    actions = Path("memory/actions/demo-actions.md")
    actions.parent.mkdir(parents=True)
    actions.write_text(
        """
# Demo Actions

| Task | Owner | Due Date | Status |
|---|---|---|---|
| Prepare token | Alex | Friday | Open |
""".strip(),
        encoding="utf-8",
    )

    output = generate_reminders(str(actions))
    text = Path(output).read_text(encoding="utf-8")

    assert "Prepare token" in text
    assert "Alex" in text


def test_send_message_dry_run():
    result = send_message("hello", dry_run=True)
    assert result["ok"] is True
    assert result["dry_run"] is True
