from datetime import date, datetime

from execution_engine.models import SessionEvent, Subtask, Task
from execution_engine.planner import AdaptivePlanner


def test_update_estimate_uses_session_average() -> None:
    task = Task("Task", planned_hours=2.0, due_date=date.today())
    task.add_session(
        SessionEvent(
            start=datetime(2026, 2, 12, 9, 0),
            end=datetime(2026, 2, 12, 11, 0),
        )
    )

    planner = AdaptivePlanner()
    estimate = planner.update_estimate(task)

    assert estimate == 2.0


def test_replan_prioritizes_due_date_and_limits_window() -> None:
    today = date(2026, 2, 12)
    soon = Task("Soon", 2.0, due_date=today)
    later = Task("Later", 2.0, due_date=date(2026, 2, 13), subtasks=[Subtask("a")])

    planner = AdaptivePlanner()
    slots = planner.replan([later, soon], datetime(2026, 2, 12, 9, 0), available_hours=3)

    assert len(slots) == 2
    assert slots[0].task_title == "Soon"
    assert round(sum(slot.estimated_hours for slot in slots), 2) == 3.0
