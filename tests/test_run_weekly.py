from __future__ import annotations

from pathlib import Path

from pmflow.workflows import run_weekly


def test_run_weekly_creates_expected_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Path("examples").mkdir()
    Path("examples/demo.md").write_text(
        """
# Demo

- Decision: keep Telegram and PowerPoint only.
- Alex will prepare Telegram token by Friday.
- Risk: Telegram noise if sent without review.
- Open question: should weekly status go to Telegram?
""".strip(),
        encoding="utf-8",
    )

    result = run_weekly("examples/demo.md", "demo", dry_run=True)

    expected_keys = {
        "protocol",
        "decisions",
        "actions",
        "outline",
        "weekly_status",
        "telegram_draft",
        "gantt",
        "pptx",
        "telegram_sent",
        "manifest",
    }
    assert expected_keys.issubset(result.keys())

    for key in expected_keys - {"telegram_sent"}:
        assert Path(result[key]).exists(), key

    assert result["telegram_sent"] == "false"
    assert "Alex" in Path(result["actions"]).read_text(encoding="utf-8")
    assert "Friday" in Path(result["actions"]).read_text(encoding="utf-8")
    gantt = Path(result["gantt"]).read_text(encoding="utf-8")
    assert "Unscheduled / Needs PM Review" in gantt
    assert "Friday" in gantt
