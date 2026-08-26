# Task Tracker Architecture and Context Experiment

## Experiment integrity note

Strategies A, B, and C were drafted with their specified context boundaries,
but they were produced during one continuing assistant conversation rather than
three isolated Codex App threads. The comparison is useful as a context-scope
review, but it is not evidence of complete conversational isolation.

## Strategy comparison

| Strategy | What it got right | What it missed or risked | Best task shape |
| --- | --- | --- | --- |
| A - minimal context | Produced a concise repository overview after inspecting the app, including the model, request flow, key files, and conventions. | The broad permission to inspect made the result accurate, but it did not reveal how much context was needed before each claim and could encourage overconfident exploration in a less familiar repository. | Early repository orientation when the agent may inspect broadly and every claim will still be reviewed. |
| B - structured context | Used `AGENTS.md` and file summaries to identify responsibilities, commands, business rules, UI states, CI, and Docker details efficiently. | Structured summaries can repeat a stale claim; important statements still need source verification. It was longer than the targeted draft. | Onboarding or cross-layer planning that needs a complete but governed repository map. |
| C - targeted context | Gave the most explicit account of what was and was not visible, and described the backend create flow without relying on frontend or test assumptions. | It could not confirm transition pairs, frontend behavior, tests, commands, CI, Docker, or dependency practices. | Focused backend analysis where honesty and a small context window matter more than whole-project completeness. |

## Verdict

Strategy B is the selected basis for the final architecture document because
the task is cross-layer onboarding: it needs backend, frontend, test, and
infrastructure context. Its structure made the result specific without treating
the whole repository as equally relevant. Strategy C remains preferable for a
narrow backend question, while Strategy A is useful for an initial discovery
pass.

## Context-engineering rule

For cross-layer onboarding or feature planning, I use structured context with
repository instructions and short file summaries because the task depends on
several components and explicit boundaries. For a focused behavior or bug, I
use targeted context with the smallest relevant source files because missing
information is easier to identify and unsupported assumptions are reduced.

## Final architecture

### Purpose and shape

Task Tracker is a Python 3.11 learning project with a FastAPI backend and a
single-file vanilla JavaScript Kanban frontend. The backend serves the UI and
JSON routes for task creation, listing and filtering, retrieval, partial
updates, and deletion. Health and version routes support verification. Tasks
are stored in process memory and disappear when the backend stops.

### Data and rules

`app/models.py` defines separate create, update, and response models. Tasks have
a title, description, status, priority, optional assignee, optional due date,
and normalized tags. Responses add UUID and UTC timestamp fields. Unknown input
fields are rejected. Titles are nonblank and limited to 200 characters; tags
are nonblank, limited to five and 30 characters each, and deduplicated without
case sensitivity.

Workflow transitions live in `app/business_rules.py`: `ToDo` to `InProgress`,
`InProgress` to `Done`, and `Done` to `InProgress`. Overdue state is computed in
storage from the due date and current status rather than persisted.

### Request flow

For task creation, `frontend/index.html` sends JSON to `POST /tasks`.
`app/main.py` receives a validated `TaskCreate`, delegates to
`app/storage.py:add_task`, and returns `TaskResponse` with HTTP 201. Storage
generates the UUID and UTC timestamps and inserts the response into `_tasks`.
The frontend then refetches tasks and rebuilds the Kanban columns.

### Responsibilities

- `app/main.py`: application, CORS, frontend response, and HTTP routes.
- `app/models.py`: data shapes, enums, and field validation.
- `app/business_rules.py`: allowed workflow transitions.
- `app/storage.py`: in-memory CRUD, timestamps, overdue logic, and filters.
- `frontend/index.html`: markup, styling, API calls, board state, modal, and
  drag-and-drop behavior.
- `tests/`: model, storage, and API verification.
- `.github/workflows/ci.yml`: Python 3.11 pytest automation.
- `Dockerfile`: non-root Python 3.11 container runtime.
- `AGENTS.md`: repository and Module 5 operating instructions.

### Conventions and limits

Run and test from the repository root with
`uvicorn app.main:app --reload --port 8000` and `pytest -v`. Validation belongs
in models, workflow rules in business rules, and persistence behavior in
storage. HTTP 404 represents missing tasks; HTTP 422 represents invalid input
or workflow changes. Frontend task text is inserted with `textContent`.

The project intentionally has no authentication, database, deployment
workflow, or production-readiness claim. Dependencies are unpinned, storage is
not persistent, and the separately served port-5500 frontend has a documented
API-base concern.

## Source drafts

- `docs/architecture-A.md`
- `docs/architecture-B.md`
- `docs/architecture-C.md`
