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
