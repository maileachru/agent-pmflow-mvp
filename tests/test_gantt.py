from __future__ import annotations

from pathlib import Path

from pmflow.gantt import generate_gantt


def test_generate_gantt_schedules_only_iso_due_dates(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    actions = Path("memory/actions/demo-actions.md")
    actions.parent.mkdir(parents=True)
    actions.write_text(
        """
# Demo Actions

| Task | Owner | Due Date | Status |
|---|---|---|---|
| Prepare launch plan | Alex | 2026-05-20 | Open |
| Confirm budget | Maria | Friday | Open |
""".strip(),
        encoding="utf-8",
    )

    output = generate_gantt("demo", str(actions))
    text = Path(output).read_text(encoding="utf-8")

    assert Path(output).exists()
    assert "Prepare launch plan" in text
    assert "2026-05-20" in text
    assert "Confirm budget" in text
    assert "Unscheduled / Needs PM Review" in text
    assert "Friday" in text
