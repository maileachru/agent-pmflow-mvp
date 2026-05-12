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


def test_action_extraction_skips_decisions_and_milestone_mentions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Path("meetings/inbox").mkdir(parents=True)
    Path("meetings/inbox/pilot.md").write_text(
        """
# Pilot

- Legal/privacy review target is 2026-05-26.
- Decision: We will run a limited pilot.
- Pilot readiness review: 2026-05-29.
- Anna will publish the pilot charter by 2026-05-13.
- Борис сделает демо до 2026-05-14.
""".strip(),
        encoding="utf-8",
    )

    result = run_weekly("meetings/inbox/pilot.md", "pilot", no_pptx=True)
    actions = Path(result["actions"]).read_text(encoding="utf-8")

    assert "publish the pilot charter" in actions
    assert "демо" in actions
    assert "Legal/privacy review target" not in actions
    assert "We | TBD" not in actions
    assert "Pilot readiness review" not in actions
