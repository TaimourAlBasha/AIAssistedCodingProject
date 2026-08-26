# Task Tracker Agent Instructions

## Project summary

This repository contains a learning-project Task Tracker. It has a FastAPI
backend, in-memory task storage, and a single-file vanilla JavaScript frontend.
The backend serves the frontend and exposes task, health, and version routes.

## Technology and commands

- Course Python version: Python 3.11
- Backend: FastAPI, Pydantic v2, and Uvicorn
- Tests: pytest, httpx, and FastAPI TestClient
- Frontend: vanilla HTML, CSS, and JavaScript
- Storage: process-local memory; tasks do not persist after restart

Run the application from the repository root:

```powershell
uvicorn app.main:app --reload --port 8000
```

Run the complete test suite:

```powershell
pytest -v
```

## Architecture

- `app/main.py`: FastAPI application, middleware, frontend route, and API routes
- `app/models.py`: request and response models and field validation
- `app/business_rules.py`: task-status transition rules
- `app/storage.py`: in-memory task operations and filtering
- `frontend/index.html`: frontend HTML, CSS, and JavaScript
- `tests/`: model, storage, and API tests
- `docs/`: project decisions, verification evidence, and course artifacts

## Confirmed business rules

- Task statuses are `ToDo`, `InProgress`, and `Done`.
- Task priorities are `Low`, `Medium`, and `High`.
- Allowed status transitions are:
  - `ToDo` to `InProgress`
  - `InProgress` to `Done`
  - `Done` to `InProgress`
- Other status transitions are rejected by the PATCH route with HTTP 422.
- Titles are trimmed, required, and limited to 200 characters.
- Unknown request fields are rejected.
- Tasks may have no more than five tags.
- Tags are trimmed, must not be blank, and are limited to 30 characters.
- Tags are deduplicated case-insensitively while preserving the first spelling.
- Due dates and assignees are optional.
- Overdue tasks have a past due date and are not in the `Done` state.

## Module 5 guardrails

- Module 5 is for grading, governance, planning, and documentation - not new app
  feature implementation.
- Prefer read-only inspection before proposing changes.
- Keep Module 5 outputs under `docs/`.
- Do not modify `app/` unless the user explicitly approves one specific,
  minimal change.
- Work on one bounded task per thread.
- Cite actual files and line numbers when making repository claims.
- Mark uncertainty clearly instead of guessing.
- Treat AI output as a draft that requires human grading.
- Do not leave placeholders in final artifacts.
- Do not implement the planned comments feature during Module 5.

## Security and governance

- Never expose or commit passwords, tokens, credentials, private keys, personal
  data, or production configuration.
- Do not run destructive commands.
- Do not add authentication, a database, deployment, or production-hardening
  claims without explicit approval.
- Distinguish intentional course limitations from confirmed vulnerabilities.
- Do not invent findings merely to fill a security-review category.
- Keep student judgments, manual findings, and personal AI rules attributable
  to the student; ask for evidence rather than fabricating them.

## Change discipline

- Preserve existing behavior outside the explicitly approved scope.
- Do not rewrite whole files for a focused correction.
- Show documentation or code diffs before applying them when requested.
- Run only verification appropriate to the change.
- Report warnings and unverified manual checks honestly.
- Do not commit or push unless the user explicitly requests it.
