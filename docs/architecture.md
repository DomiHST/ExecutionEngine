# Architecture Overview

This document translates the supplied PRD to an executable baseline.

## Core capabilities

1. **Today View**
   - Shows all tasks, subtasks, notes and reminders relevant for the current day.
   - Includes status badges:
     - `⚠️` for low LLM confidence score.
     - `🔹` for incomplete subtasks.
2. **Adaptive Task Duration Learning**
   - Every session contributes to historical durations.
   - Average durations are used to update planning estimates.
3. **Dynamic Rescheduling**
   - Open tasks are sorted and packed into available time windows.
4. **Portable File Storage**
   - Markdown content remains human-readable.
   - Metadata in JSON enables quick loading and indexing.

## Storage mapping

The code models this structure:

```text
life_system/
├─ inbox/
├─ projects/
│  ├─ work_opportunities/
│  ├─ work_projects/
│  ├─ private_projects/
│  └─ prive_contacts/
├─ metadata/
├─ views/
└─ config/
```

## Module boundaries

- `models.py`
  - Data entities: project, contact, note, task, subtask, session event.
- `planner.py`
  - Duration updates from sessions.
  - Replanning function for open tasks.
- `today_view.py`
  - Rendering logic for direct, filterless Today View output.
- `example.py`
  - Demonstrates the flow without external services.

## Next implementation steps

- Add markdown and JSON loaders/writers for full file roundtrips.
- Add a PySide6 tray shell connected to these modules.
- Add LLM masking/unmasking adapter interface and cloud providers.
