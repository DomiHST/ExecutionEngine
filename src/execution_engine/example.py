from __future__ import annotations

from datetime import date, datetime, time, timedelta

from .models import Category, Note, Project, SessionEvent, Subtask, Task
from .planner import AdaptivePlanner
from .today_view import render_today_view


def build_sample() -> list[Project]:
    duo = Project(
        project_id="work-20260213-duo",
        name="Project: DUO Demo",
        category=Category.WORK_PROJECT,
        notes=[
            Note("Feedback klant meeting", "Slides te gedetailleerd", informational=True, llm_score=0.88),
            Note("Slides aangepast", "Kernpunten toegevoegd", informational=False, llm_score=0.96),
        ],
    )

    slides = Task(
        title="Slides controleren",
        planned_hours=2.75,
        due_date=date.today(),
        subtasks=[Subtask("check formatting"), Subtask("finalize content", done=True)],
    )
    slides.add_session(
        SessionEvent(
            start=datetime.combine(date.today(), time(9, 0)),
            end=datetime.combine(date.today(), time(10, 30)),
        )
    )

    demo = Task(
        title="Demo script oefenen",
        planned_hours=1.0,
        due_date=date.today(),
        subtasks=[Subtask("update slides")],
    )
    duo.tasks.extend([slides, demo])

    esp = Project(
        project_id="private-20260212-esp32",
        name="Project: Side Project ESP32",
        category=Category.PRIVATE_PROJECT,
        tasks=[
            Task("Web UI design review", 1.0, date.today(), subtasks=[Subtask("layout check")]),
            Task("Dot matrix display test", 1.0, date.today(), subtasks=[Subtask("LED patterns")]),
        ],
    )

    planner = AdaptivePlanner()
    planner.replan(duo.tasks + esp.tasks, datetime.now(), available_hours=6)
    return [duo, esp]


if __name__ == "__main__":
    print(render_today_view(build_sample(), date.today()))
