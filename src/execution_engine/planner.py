from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .models import Task


@dataclass(slots=True)
class PlannedSlot:
    task_title: str
    start: datetime
    end: datetime
    estimated_hours: float


class AdaptivePlanner:
    """Learns durations from session logs and replans open tasks."""

    def update_estimate(self, task: Task) -> float:
        historical_avg = task.average_session_hours()
        if historical_avg is not None:
            task.planned_hours = round((task.planned_hours + historical_avg) / 2, 2)
        return task.planned_hours

    def replan(
        self,
        tasks: list[Task],
        window_start: datetime,
        available_hours: float,
    ) -> list[PlannedSlot]:
        open_tasks = [task for task in tasks if not task.done]
        prioritized = sorted(
            open_tasks,
            key=lambda task: (
                task.due_date is None,
                task.due_date,
                -1 if task.has_incomplete_subtasks() else 0,
            ),
        )

        slots: list[PlannedSlot] = []
        cursor = window_start
        remaining = available_hours

        for task in prioritized:
            estimate = self.update_estimate(task)
            if remaining <= 0:
                break
            slot_hours = min(estimate, remaining)
            slot_end = cursor + timedelta(hours=slot_hours)
            slots.append(
                PlannedSlot(
                    task_title=task.title,
                    start=cursor,
                    end=slot_end,
                    estimated_hours=slot_hours,
                )
            )
            cursor = slot_end
            remaining = round(remaining - slot_hours, 4)

        return slots
