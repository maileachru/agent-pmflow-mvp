from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActionItem:
    task: str
    owner: str = "TBD"
    due_date: str = "TBD"
    status: str = "Open"


@dataclass(frozen=True)
class Decision:
    text: str
    rationale: str = "TBD"
    owner: str = "TBD"
    date: str = "TBD"
