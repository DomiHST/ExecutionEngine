from datetime import date

from execution_engine.models import Category, Note, Project, Subtask, Task
from execution_engine.today_view import render_today_view


def test_today_view_contains_badges_and_sections() -> None:
    project = Project(
        project_id="work-1",
        name="Project: DUO Demo",
        category=Category.WORK_PROJECT,
        tasks=[Task("Slides controleren", 2.75, due_date=date(2026, 2, 12), subtasks=[Subtask("check formatting")])],
        notes=[Note("Feedback", "detail", llm_score=0.88)],
    )

    output = render_today_view([project], date(2026, 2, 12))

    assert "TODAY VIEW - 2026-02-12" in output
    assert "WORK PROJECTS" in output
    assert "⚠️ 1 low_score" in output
    assert "🔹 check formatting" in output
