from __future__ import annotations

from pathlib import Path

from pmflow.backlog import backlog_template
from pmflow.cli import main


def test_backlog_schema_and_example_exist():
    assert Path("backlog/schema/backlog-item.schema.yaml").exists()
    assert Path("backlog/examples/backlog-item.example.yaml").exists()


def test_backlog_example_contains_project_id():
    example = Path("backlog/examples/backlog-item.example.yaml").read_text(encoding="utf-8")

    assert "project_id: pulse-youth-alumni" in example


def test_backlog_template_command_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        [
            "pmflow",
            "backlog-template",
            "--project-id",
            "pulse-youth-alumni",
            "--title",
            "Модуль Мероприятия",
        ],
    )

    main()

    generated = Path("backlog/normalized/pulse-youth-alumni-backlog-item.yaml")
    assert generated.exists()
    assert generated.name.isascii()


def test_generated_backlog_template_contains_project_id(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    output_path = backlog_template("pulse-youth-alumni", "Модуль Мероприятия")
    content = Path(output_path).read_text(encoding="utf-8")

    assert "project_id: pulse-youth-alumni" in content
    assert "title: Модуль Мероприятия" in content


def _write_backlog_item(
    root: Path,
    project_id: str,
    item_id: str,
    *,
    title: str,
    status: str = "new",
    quarter: str = "2026-Q2",
    estimate_value: str = "3",
    estimate_unit: str = "days",
    owner: str = "Owner",
    priority: str = "medium",
    due: str = "2026-06-30",
    risks: list[str] | None = None,
    open_questions: list[str] | None = None,
    pgk_required: bool = False,
    alumni_applicable: bool = False,
) -> Path:
    risks = risks or []
    open_questions = open_questions or []
    risk_lines = "\n".join(f"  - {risk}" for risk in risks) or "[]"
    question_lines = "\n".join(f"  - {question}" for question in open_questions) or "[]"
    path = root / "backlog" / "normalized" / f"{project_id}-{item_id}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""
id: {item_id}
project_id: {project_id}
title: {title}
description: TBD
type: task
status: {status}
priority: {priority}
owner: {owner}
estimate:
  value: {estimate_value}
  unit: {estimate_unit}
dates:
  created: null
  updated: null
  start: null
  due: {due}
  quarter: {quarter}
acceptance_criteria: []
definition_of_done: []
success_metrics: []
dependencies: []
risks: {risk_lines if risk_lines == '[]' else ''}
{risk_lines if risk_lines != '[]' else ''}
open_questions: {question_lines if question_lines == '[]' else ''}
{question_lines if question_lines != '[]' else ''}
custom_fields:
  pgk_required: {str(pgk_required).lower()}
  alumni_applicable: {str(alumni_applicable).lower()}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return path


def test_backlog_report_creates_quality_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_backlog_item(
        tmp_path,
        "campus-career-hub",
        "events",
        title="Events Module MVP",
        risks=["Scope is not confirmed"],
        open_questions=["Confirm MVP scope"],
        pgk_required=True,
        alumni_applicable=True,
    )
    monkeypatch.setattr("sys.argv", ["pmflow", "backlog-report", "--project-id", "campus-career-hub"])

    main()

    report = Path("backlog/reports/campus-career-hub-quality-report.md")
    assert report.exists()
    content = report.read_text(encoding="utf-8")
    assert "## Total items\n\n1" in content
    assert "## Items with risks" in content
    assert "events" in content


def test_roadmap_report_creates_roadmap(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_backlog_item(tmp_path, "campus-career-hub", "events", title="Events Module MVP")
    monkeypatch.setattr("sys.argv", ["pmflow", "roadmap-report", "--project-id", "campus-career-hub"])

    main()

    roadmap = Path("backlog/roadmap/campus-career-hub-roadmap.md")
    assert roadmap.exists()
    content = roadmap.read_text(encoding="utf-8")
    assert "## 2026-Q2" in content
    assert "| ID | Title | Owner | Priority | Estimate | Target End | Status |" in content
    assert "Events Module MVP" in content


def test_executive_report_creates_executive_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_backlog_item(tmp_path, "campus-career-hub", "events", title="Events Module MVP")
    Path("outputs/status").mkdir(parents=True)
    Path("outputs/status/demo-weekly-status.md").write_text("# Weekly Status\n", encoding="utf-8")
    Path("outputs/demo-manifest.txt").write_text("weekly_status: outputs/status/demo-weekly-status.md\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["pmflow", "backlog-report", "--project-id", "campus-career-hub"])
    main()
    monkeypatch.setattr("sys.argv", ["pmflow", "roadmap-report", "--project-id", "campus-career-hub"])
    main()
    monkeypatch.setattr(
        "sys.argv",
        ["pmflow", "executive-report", "--project-id", "campus-career-hub", "--title", "Campus Career Hub"],
    )

    main()

    report = Path("outputs/reports/campus-career-hub-executive-report.md")
    assert report.exists()
    content = report.read_text(encoding="utf-8")
    assert "# Executive Report — Campus Career Hub" in content
    assert "## Overall Status" in content
    assert "Latest weekly status: `outputs/status/demo-weekly-status.md`" in content


def test_reports_filter_by_project_id(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_backlog_item(tmp_path, "campus-career-hub", "events", title="Events Module MVP")
    _write_backlog_item(tmp_path, "other-project", "billing", title="Billing Module")
    monkeypatch.setattr("sys.argv", ["pmflow", "backlog-report", "--project-id", "campus-career-hub"])

    main()

    content = Path("backlog/reports/campus-career-hub-quality-report.md").read_text(encoding="utf-8")
    assert "Events Module MVP" in content
    assert "Billing Module" not in content
    assert "## Total items\n\n1" in content


def test_reports_do_not_mix_backlog_items_from_different_projects(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_backlog_item(tmp_path, "campus-career-hub", "events", title="Events Module MVP", quarter="2026-Q2")
    _write_backlog_item(tmp_path, "other-project", "billing", title="Billing Module", quarter="2026-Q3")
    monkeypatch.setattr("sys.argv", ["pmflow", "roadmap-report", "--project-id", "campus-career-hub"])

    main()

    content = Path("backlog/roadmap/campus-career-hub-roadmap.md").read_text(encoding="utf-8")
    assert "Events Module MVP" in content
    assert "Billing Module" not in content
    assert "2026-Q3" not in content
