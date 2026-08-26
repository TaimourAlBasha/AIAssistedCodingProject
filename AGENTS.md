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

## Final-project guardrails

- The final project hardens, verifies, documents, reviews, and governs the
  existing Task Tracker. It does not add product features.
- Prefer read-only inspection before proposing changes.
- Do not add comments, authentication, a database, notifications, deployment,
  or major UI changes.
- Modify `app/` or `frontend/` only for a specific, minimal correction approved
  by the user, and explain that correction in `docs/final-ai-review.md`.
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

Never commit:

- `.env` files, credentials, tokens, passwords, or private keys
- production logs, customer data, or personal account/session information
- `venv/`, `.venv/`, caches, build output, editor files, or OS metadata
- assignment PDFs, temporary exports, or AI planning files with unfinished
  placeholders

## Coding and testing expectations

- Keep validation in `app/models.py`, transition rules in
  `app/business_rules.py`, storage behavior in `app/storage.py`, and routes in
  `app/main.py`.
- Preserve public route and model names unless a requested change requires a
  documented contract update.
- Add or update focused tests for changed behavior, then run the complete suite
  with `pytest -v`.
- Supplement automated checks with a browser check for user-visible behavior.
- For Docker changes, verify the build, `/health`, and non-root runtime user.

## Documentation expectations

- Keep commands copy-pasteable from the repository root.
- Update README when startup, testing, Docker, CI, structure, or limitations
  change.
- Record final verification in `docs/release-evidence.md`, AI review and
  security triage in `docs/final-ai-review.md`, and personal working rules in
  `docs/ai-playbook.md`.
- Separate automated evidence from human observations and never claim a check
  that was not performed.

## Change discipline

- Preserve existing behavior outside the explicitly approved scope.
- Do not rewrite whole files for a focused correction.
- Show documentation or code diffs before applying them when requested.
- Run only verification appropriate to the change.
- Report warnings and unverified manual checks honestly.
- Do not commit or push unless the user explicitly requests it.

## Definition of done

A final-project change is done only when its scope is clear, the diff contains
no unrelated files, relevant focused checks and `pytest -v` pass, documented
commands match the repository, privacy and placeholder scans are clean, and
any required browser or Docker evidence is recorded. Before submission, confirm
that the `final-project` branch is pushed and its GitHub Actions run is green.
