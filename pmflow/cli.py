from __future__ import annotations

import argparse
from pathlib import Path

from .processor import process_meeting
from .status import generate_weekly_status
from .telegram import generate_reminders, send_message
from .pptx_export import export_pptx
from .gantt import generate_gantt
from .workflows import run_weekly


def print_result(result: dict[str, str]) -> None:
    for key, value in result.items():
        print(f"{key}: {value}")


def doctor() -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "skills/meeting-protocol-generation/SKILL.md",
        "skills/stakeholder-status-reporting/SKILL.md",
        "skills/presentation-generation/SKILL.md",
        "skills/project-planning-gantt/SKILL.md",
        "integrations/telegram/README.md",
        "integrations/powerpoint/README.md",
        "templates/gantt-template.md",
        "docs/AGENT_COMPATIBILITY.md",
        "docs/PM_SKILLS.md",
    ]
    missing = [p for p in required if not Path(p).exists()]
    if missing:
        print("Missing files:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)

    print("Agent PMFlow MVP is ready.")


def demo() -> None:
    result = run_weekly("examples/demo-meeting.md", "demo", send_telegram=False)
    print_result(result)


def main() -> None:
    parser = argparse.ArgumentParser(prog="pmflow")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    sub.add_parser("demo")

    p_run = sub.add_parser("run-weekly")
    p_run.add_argument("--meeting", required=True)
    p_run.add_argument("--title", default=None)
    p_run.add_argument("--send-telegram", action="store_true")
    p_run.add_argument("--dry-run", action="store_true")
    p_run.add_argument("--no-pptx", action="store_true")
    p_run.add_argument("--telegram-message-limit", type=int, default=20)

    p_meeting = sub.add_parser("process-meeting")
    p_meeting.add_argument("input")
    p_meeting.add_argument("--title", default=None)

    p_status = sub.add_parser("weekly-status")
    p_status.add_argument("--title", default="weekly-status")
    p_status.add_argument("--actions", default=None)
    p_status.add_argument("--decisions", default=None)

    p_reminders = sub.add_parser("telegram-reminders")
    p_reminders.add_argument("--actions", required=True)
    p_reminders.add_argument("--message-limit", type=int, default=20)

    p_send = sub.add_parser("telegram-send")
    p_send.add_argument("--message", required=True)
    p_send.add_argument("--dry-run", action="store_true")

    p_pptx = sub.add_parser("pptx")
    p_pptx.add_argument("--outline", required=True)
    p_pptx.add_argument("--output", required=True)

    p_gantt = sub.add_parser("gantt")
    p_gantt.add_argument("--title", default="project-plan")
    p_gantt.add_argument("--actions", required=True)

    args = parser.parse_args()

    if args.command == "doctor":
        doctor()
    elif args.command == "demo":
        demo()
    elif args.command == "run-weekly":
        result = run_weekly(
            meeting=args.meeting,
            title=args.title,
            send_telegram=args.send_telegram,
            dry_run=args.dry_run,
            no_pptx=args.no_pptx,
            telegram_message_limit=args.telegram_message_limit,
        )
        print_result(result)
    elif args.command == "process-meeting":
        print_result(process_meeting(args.input, args.title))
    elif args.command == "weekly-status":
        print(generate_weekly_status(args.title, args.actions, args.decisions))
    elif args.command == "telegram-reminders":
        print(generate_reminders(args.actions, args.message_limit))
    elif args.command == "telegram-send":
        print(send_message(args.message, dry_run=args.dry_run))
    elif args.command == "pptx":
        print(export_pptx(args.outline, args.output))
    elif args.command == "gantt":
        print(generate_gantt(args.title, args.actions))


if __name__ == "__main__":
    main()
