# Architecture Strategy C - Targeted Context

## Context boundary

This draft uses only `app/main.py`, `app/models.py`, and `app/storage.py`.
Information not established by those files is labeled as not visible rather
than inferred from other repository knowledge.

## What the app does

The application is a FastAPI Task Tracker API that also serves a fixed
`frontend/index.html` file at `/`. Visible endpoints report health and version,
create and list tasks, retrieve one task, partially update a task, and delete a
task. Task data is held in a module-level dictionary, so persistence beyond the
running process is not visible from the files read.

## Data model

`TaskCreate` accepts title, description, status, priority, assignee, due date,
and tags. `TaskUpdate` makes those fields optional for partial updates.
`TaskResponse` adds string ID and datetime fields. Status values are `ToDo`,
`InProgress`, and `Done`; priorities are `Low`, `Medium`, and `High`.

Titles are stripped, nonblank, and at most 200 characters. Tags are stripped,
nonblank, at most 30 characters each, case-insensitively deduplicated, and
limited to five normalized values. Extra model fields are forbidden.

## Request flow: create a task

1. A client sends JSON to `POST /tasks`.
2. FastAPI parses and validates the body as `TaskCreate`.
3. The route calls `storage.add_task`.
4. Storage creates a UUID string and one timezone-aware UTC timestamp for both
   `created_at` and `updated_at`.
5. Storage creates `TaskResponse`, adds it to `_tasks`, and returns it.
6. FastAPI returns the response model with HTTP 201.

What the frontend does after receiving the response is not visible from the
files read.

## Key files

- `app/main.py`: application setup, CORS, frontend response, and API handlers.
- `app/models.py`: task enums, models, and field validation.
- `app/storage.py`: in-memory CRUD, overdue calculation, and filters.
- `app/business_rules.py`: referenced by `app/main.py` for status validation,
  but its actual transition set is not visible from the files read.
- `frontend/index.html`: referenced by `app/main.py`, but its structure and
  behavior are not visible from the files read.

Test, dependency, Docker, CI, and documentation files are not visible from the
selected context.

## Conventions

- Routes use Pydantic request and response models.
- Missing task lookups return HTTP 404.
- Blank tag filters and invalid status changes return HTTP 422.
- PATCH passes only explicitly supplied fields to storage, preserves unchanged
  tasks, and updates `updated_at` only when a value changes.
- Storage generates UUID4 identifiers and timezone-aware UTC timestamps.
- Overdue state is computed from a date-only due date, the local current date,
  and whether status is not `Done`.
- CORS explicitly permits localhost origins on port 5500 and the listed HTTP
  methods.

## Not visible or assumptions

- The exact allowed status-transition pairs are not visible because
  `app/business_rules.py` was not read.
- Frontend interaction, rendering safety, UI states, and API-base selection are
  not visible from the files read.
- Test framework, test coverage, and reset fixtures are not visible.
- Supported run and test commands are not visible.
- Docker, CI, dependency versions, and Python course version are not visible.
- Authentication, deployment, and production requirements are not visible.

## Files read

- `app/main.py`
- `app/models.py`
- `app/storage.py`

## What this targeted strategy likely missed

It captures the backend request and storage path accurately but cannot provide
a reliable onboarding view of workflow rules, frontend behavior, tests,
commands, dependency management, or infrastructure.
