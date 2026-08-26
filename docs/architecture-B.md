# Architecture Strategy B - Structured Context

## What the app does

Task Tracker is a Python 3.11 course project combining a FastAPI backend with a
single-file vanilla JavaScript Kanban board. The backend serves the board at
`/`, exposes health and version information, and provides CRUD-style task
routes. Tasks support workflow states, priorities, optional assignees and due
dates, normalized tags, overdue filtering, modal editing, drag-and-drop status
changes, and visible invalid-transition feedback. Storage is process-local and
is cleared when the backend stops.

## Data model

`app/models.py` separates `TaskCreate`, `TaskUpdate`, and `TaskResponse`.
Requests reject unknown fields. A task has a required trimmed title, optional
description and assignee, status and priority enums, optional date-only due
date, and up to five tags of at most 30 characters. Tags are trimmed and
deduplicated case-insensitively while preserving the first spelling. Responses
add a UUID string and timezone-aware creation/update timestamps.

The workflow accepts `ToDo` to `InProgress`, `InProgress` to `Done`, and `Done`
to `InProgress`. Other PATCH status pairs are rejected. Overdue state is
computed rather than stored: the due date is before the local current date and
the task is not `Done`.

## Request flow: create a task

1. `frontend/index.html` sends task JSON to `POST /tasks` using `fetch`.
2. `app/main.py` asks FastAPI/Pydantic to parse `TaskCreate`.
3. `app/models.py` applies enum, date, title, tag, and extra-field rules.
4. The route delegates to `app/storage.py:add_task`.
5. Storage creates UUID and UTC timestamp values, constructs `TaskResponse`,
   and inserts it into `_tasks`.
6. The route returns the response model with HTTP 201.
7. The frontend closes the modal and refetches tasks before rendering columns.

## Key files

- `AGENTS.md`: repository instructions, commands, business rules, and Module 5
  boundaries.
- `app/main.py`: FastAPI setup, CORS, static frontend response, and API routes.
- `app/models.py`: enums, request/response shapes, and field validation.
- `app/business_rules.py`: explicit status-transition set and HTTP 422 failure.
- `app/storage.py`: in-memory CRUD, overdue calculation, and combined filters.
- `frontend/index.html`: all frontend structure, presentation, state, and API
  interaction.
- `tests/test_models.py`: create/update validation tests.
- `tests/test_storage.py`: storage behavior and reset isolation.
- `tests/test_tasks.py`: API, due-date, tag, filter, and transition tests.
- `.github/workflows/ci.yml`: Python 3.11 dependency installation and pytest.

## Conventions

- The course commands are `uvicorn app.main:app --reload --port 8000` and
  `pytest -v` from the repository root.
- Model validation belongs in `app/models.py`; transition rules belong in
  `app/business_rules.py`; storage behavior belongs in `app/storage.py`.
- API handlers return response models and use HTTP 404 for missing tasks and
  HTTP 422 for validation or workflow rejection.
- PATCH distinguishes omitted fields from explicitly cleared values through
  Pydantic's supplied-field tracking.
- Frontend rendering uses DOM nodes and `textContent`; loading, empty, error,
  modal-validation, and transition-toast states are visible.
- CI tests on pushes and pull requests; Docker runs Uvicorn as non-root user
  `app` without reload.

## Not visible or assumptions

- Expected scale, concurrency, service-level requirements, and deployment
  target are not defined.
- There is intentionally no authentication, database, or deployment workflow.
- Dependency versions are not pinned, so the exact installed environment is
  not determined by `requirements.txt` alone.
- The frontend behavior when served separately on port 5500 has a documented
  API-base concern that is not resolved by this architecture description.

## Which structured context helped most

`AGENTS.md` helped most because it maps each responsibility to a file and
states the verified business rules and Module 5 boundaries in one place. The
file summaries then made it efficient to confirm those claims in source.

## Remaining assumptions or unsupported details

No claims are made about production traffic, persistence, identities,
deployment, or future feature ownership because those are not defined by the
structured context or inspected files.
