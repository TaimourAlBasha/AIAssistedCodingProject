# CLAUDE.md

## 1. Tech stack

- Python 3.11 (declared in `.github/workflows/ci.yml`)
- FastAPI
- Pydantic v2 APIs (`ConfigDict` and `field_validator`); the dependency version is not pinned
- Uvicorn
- pytest
- httpx
- Vanilla JavaScript frontend in `frontend/index.html`
- In-memory task storage

Dependency versions are not pinned in `requirements.txt`.

## 2. Run command

Run the application from the repository root using the course command:

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend serves `frontend/index.html` at `http://127.0.0.1:8000/`.

## 3. Test command

Run the complete test suite from the repository root using the course command:

```powershell
pytest -v
```

## 4. Architecture summary

- `app/main.py`: FastAPI application, middleware, frontend route, health route, and task API routes.
- `app/models.py`: task request and response models, enums, and field validation.
- `app/business_rules.py`: allowed task-status transitions and transition validation.
- `app/storage.py`: in-memory task storage operations used by the API routes.
- `frontend/index.html`: single-file vanilla JavaScript frontend containing its HTML, CSS, and JavaScript.
- `tests/test_models.py`: model validation tests.
- `tests/test_storage.py`: storage tests.
- `tests/test_tasks.py`: API route and task-behavior tests.
- `docs/midcourse/`: project decisions, prompts, verification evidence, user stories, and reflection.

Task transition rules live in `app/business_rules.py`. Task field rules, including title and tag validation, live in `app/models.py`.

## 5. Business rules

Task status values are:

- `ToDo`
- `InProgress`
- `Done`

The implemented allowed transitions are:

- `ToDo` -> `InProgress`
- `InProgress` -> `Done`
- `Done` -> `InProgress`

Any other transition, including `InProgress` -> `ToDo`, `Done` -> `ToDo`, and same-status transitions, is rejected with HTTP 422 when status is supplied to `PATCH /tasks/{task_id}`.

## 6. UI states and CORS notes

The frontend implements `loading`, `ready`, `empty`, and `error` board states. It also includes:

- Empty-column and no-filter-match messages
- A retry action when task loading fails
- A modal for creating and editing tasks
- Inline modal validation errors
- Drag-and-drop status updates
- An alert toast when a drag-and-drop transition fails
- Overdue and tag filters

CORS allows `http://localhost:5500` and `http://127.0.0.1:5500`. Allowed methods are `GET`, `POST`, `PATCH`, `DELETE`, and `OPTIONS`; credentials and all request headers are allowed.

## 7. Do-not rules

- Do not add authentication without asking first.
- Do not add a database or replace the in-memory storage without asking first.
- Do not add deployment configuration or deployment steps without asking first.
- Do not make major UI changes or introduce a frontend framework without asking first.
