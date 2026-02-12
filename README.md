# Personal Execution System

Initial implementation for the PRD:

- File-based domain model for projects, contacts, notes, tasks and subtasks.
- Today View aggregation with badges (`⚠️` low score, `🔹` incomplete subtasks).
- Start/Stop session tracking primitives for adaptive task duration learning.
- Dynamic rescheduling helper based on historical task duration averages.

## Quick start

```bash
python -m execution_engine.example
```

## Repository layout

- `src/execution_engine/models.py`: domain models.
- `src/execution_engine/planner.py`: adaptive duration + dynamic replanning.
- `src/execution_engine/today_view.py`: ASCII Today View renderer.
- `docs/architecture.md`: architecture and storage mapping from PRD.
- `tests/`: core planning and rendering tests.
