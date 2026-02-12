from __future__ import annotations

from datetime import date

from .models import Category, Project

CATEGORY_LABELS = {
    Category.WORK_OPPORTUNITY: "WORK OPPORTUNITIES",
    Category.WORK_PROJECT: "WORK PROJECTS",
    Category.PRIVATE_PROJECT: "PRIVE PROJECTS",
    Category.PRIVATE_CONTACT: "PRIVE CONTACTS",
}


def render_today_view(projects: list[Project], day: date) -> str:
    lines: list[str] = []
    lines.append(f"TODAY VIEW - {day.isoformat()}")
    lines.append("=" * 59)

    for category in Category:
        grouped = [project for project in projects if project.category == category]
        if not grouped:
            continue

        lines.append(CATEGORY_LABELS[category])
        lines.append("-" * 59)

        for project in grouped:
            low_scores = project.low_score_count()
            low_score_badge = f"⚠️ {low_scores} low_score" if low_scores else "OK"
            lines.append(f"{project.name}  | Status: {low_score_badge}")

            lines.append("Tasks / Subtasks")
            for task in project.tasks_for_day(day):
                planned = f"planned {task.planned_hours}h"
                lines.append(f" [ ] {task.title} ({planned})")
                for subtask in task.subtasks:
                    icon = "[x]" if subtask.done else "🔹"
                    lines.append(f"    {icon} {subtask.title}")

            if project.notes:
                lines.append("Notes")
            for note in project.notes:
                prefix = "⚠️" if note.low_score else "+"
                kind = "Informational" if note.informational else "Task-linked"
                lines.append(f" [{prefix}] {kind}: {note.title}")

            lines.append("-" * 59)

    lines.append("Buttons: [ + Nieuwe Notitie ] [ Request Info ] [ Refresh ]")
    return "\n".join(lines)
