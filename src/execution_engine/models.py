from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from statistics import mean


class Category(str, Enum):
    WORK_OPPORTUNITY = "work_opportunity"
    WORK_PROJECT = "work_project"
    PRIVATE_PROJECT = "private_project"
    PRIVATE_CONTACT = "private_contact"


@dataclass(slots=True)
class Subtask:
    title: str
    done: bool = False


@dataclass(slots=True)
class SessionEvent:
    start: datetime
    end: datetime

    @property
    def duration(self) -> timedelta:
        return self.end - self.start


@dataclass(slots=True)
class Task:
    title: str
    planned_hours: float
    due_date: date | None = None
    done: bool = False
    subtasks: list[Subtask] = field(default_factory=list)
    sessions: list[SessionEvent] = field(default_factory=list)

    def has_incomplete_subtasks(self) -> bool:
        return any(not sub.done for sub in self.subtasks)

    def add_session(self, session: SessionEvent) -> None:
        self.sessions.append(session)

    def average_session_hours(self) -> float | None:
        if not self.sessions:
            return None
        return mean([s.duration.total_seconds() / 3600 for s in self.sessions])


@dataclass(slots=True)
class Note:
    title: str
    content: str
    informational: bool = True
    llm_score: float = 1.0

    @property
    def low_score(self) -> bool:
        return self.llm_score < 0.9


@dataclass(slots=True)
class Project:
    project_id: str
    name: str
    category: Category
    tasks: list[Task] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)

    def low_score_count(self) -> int:
        return sum(1 for note in self.notes if note.low_score)

    def tasks_for_day(self, day: date) -> list[Task]:
        return [
            task
            for task in self.tasks
            if not task.done and (task.due_date is None or task.due_date <= day)
        ]
