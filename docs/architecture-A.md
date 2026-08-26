# Architecture Strategy A - Minimal Context

## What the app does

Task Tracker is a learning-project Kanban application. A FastAPI backend serves
both a vanilla JavaScript task board and JSON endpoints for creating, listing,
filtering, reading, partially updating, and deleting tasks. It also exposes
health and version endpoints. Task data lasts only for the life of the backend
process.

## Data model

The central entity is a task. Client-created fields are title, description,
status, priority, assignee, due date, and tags. The server adds a UUID string,
creation timestamp, and update timestamp. Status is limited to `ToDo`,
`InProgress`, and `Done`; priority is limited to `Low`, `Medium`, and `High`.
Titles and tags have explicit validation, and unknown request fields are
rejected. Create, partial-update, and response models are separate.

## Request flow: create a task

1. The browser submits JSON to `POST /tasks`.
2. FastAPI parses the body into `TaskCreate`.
3. Pydantic rejects unknown fields and validates the title, enums, date, and
   tags.
4. The route calls `storage.add_task`.
5. Storage generates a UUID and UTC timestamps, builds `TaskResponse`, and
   inserts it into the module-level task dictionary.
6. FastAPI serializes the response model and returns HTTP 201.
7. The frontend refreshes its task list and rerenders the board.

## Key files

- `app/main.py`: application construction, CORS, frontend serving, and routes.
- `app/models.py`: task enums, Pydantic request/response models, and validation.
- `app/business_rules.py`: allowed status-transition pairs.
- `app/storage.py`: process-local task dictionary, CRUD, and filters.
- `frontend/index.html`: board markup, styles, API calls, modal, filters, and
  drag-and-drop behavior.
- `tests/test_models.py`: request-model validation tests.
- `tests/test_storage.py`: in-memory storage tests.
- `tests/test_tasks.py`: TestClient API and feature tests.
- `requirements.txt`: unpinned Python package names.
- `.github/workflows/ci.yml`: Python 3.11 pytest workflow.

## Conventions

- Routes validate transport input with Pydantic and delegate persistence to
  `app/storage.py`.
- Workflow transitions are checked separately in `app/business_rules.py`.
- PATCH uses `exclude_unset=True`, preserving omitted fields while allowing
  supported fields such as due dates and tags to be cleared.
- Missing task identifiers produce HTTP 404; validation and invalid transitions
  produce HTTP 422.
- The frontend uses `fetch`, creates DOM nodes, and places task text through
  `textContent`.
- Tests reset module storage around cases to avoid state leakage.

## Not visible or assumptions

- There is no database, authentication, deployment workflow, or production
  hardening in the inspected repository.
- Expected concurrent-user volume and hosting environment are not defined.
- Product rules for comment authors, task ownership, and persistence are not
  part of the current application.

## Files inspected

`README.md`, `app/main.py`, `app/models.py`, `app/business_rules.py`,
`app/storage.py`, `frontend/index.html`, the three test files,
`requirements.txt`, and `.github/workflows/ci.yml`.

## Assumptions or possible inventions

The application description and request flow are supported by the inspected
files. User volume, deployment environment, and future ownership rules remain
unknown rather than inferred.
