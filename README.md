# Task Tracker

## Project overview

Task Tracker is a learning-project Kanban application with a FastAPI backend
and a vanilla JavaScript frontend. It supports creating, viewing, editing,
filtering, moving, and deleting tasks.

Current task features include:

- `ToDo`, `InProgress`, and `Done` workflow states
- Controlled status transitions
- Priorities and optional assignees
- Optional due dates and overdue filtering
- Up to five normalized tags per task
- Case-insensitive tag filtering
- Drag-and-drop task movement
- Modal-based task creation and editing
- Visible feedback for invalid transitions

The backend serves the frontend directly. API documentation is available at
<http://127.0.0.1:8000/docs>.

## Prerequisites

- Python 3.11
- `pip`
- PowerShell for the commands shown below
- Docker Desktop with Linux containers enabled, when using Docker
- Git, when working with branches or GitHub Actions

## Local setup

Run these commands from the repository root:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Dependencies are currently unpinned in `requirements.txt`.

## Run the app locally

Activate the virtual environment, if it is not already active:

```powershell
.\venv\Scripts\Activate.ps1
```

Start the development server with the course command:

```powershell
uvicorn app.main:app --reload --port 8000
```

Open the following addresses:

- Task board: <http://127.0.0.1:8000/>
- API documentation: <http://127.0.0.1:8000/docs>
- Health endpoint: <http://127.0.0.1:8000/health>
- Version endpoint: <http://127.0.0.1:8000/version>

You can check the service from PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/version
```

## Run tests

Run the complete test suite from the repository root:

```powershell
pytest -v
```

The tests cover request models, in-memory storage, API behavior, due dates,
tags, filters, and task status transitions.

## Run with Docker

Docker uses a multi-stage Python 3.11 slim build. The runtime image starts the
API as the non-root `app` user and does not use development reload mode.

Build the image:

```powershell
docker build -t task-tracker:dev .
```

Start the container and publish port 8000:

```powershell
docker run --detach --name tt-dev --publish 8000:8000 task-tracker:dev
```

Verify the application, container health, and runtime user:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
docker inspect tt-dev --format '{{.State.Health.Status}}'
docker exec tt-dev whoami
```

Expected evidence is a health response containing `"status": "ok"`, Docker
health status `healthy`, and runtime user `app`.

Remove the local verification container when finished:

```powershell
docker rm --force tt-dev
```

Docker build and runtime verification have passed with the commands above.

## CI workflow summary

The workflow at `.github/workflows/ci.yml` runs on every push and pull request.
It:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Upgrades `pip`.
4. Installs `requirements.txt`.
5. Runs `pytest -v`.

The workflow performs testing only. It contains no deployment steps and does
not suppress pytest failures.

## Project structure

```text
task-tracker-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── business_rules.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
├── docs/
│   └── midcourse/
├── frontend/
│   └── index.html
├── tests/
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_tasks.py
├── .dockerignore
├── CLAUDE.md
├── Dockerfile
├── README.md
└── requirements.txt
```

- `app/main.py` defines the FastAPI application and routes.
- `app/models.py` contains request and response models and field validation.
- `app/business_rules.py` contains task status transition rules.
- `app/storage.py` contains in-memory task operations and filters.
- `frontend/index.html` contains the frontend HTML, CSS, and JavaScript.
- `tests/` contains model, storage, and API tests.
- `docs/decisions/` contains technical decision notes.
- `docs/module4/` contains Module 4 verification evidence.
- `docs/midcourse/` contains project decisions and learning evidence.

## Project conventions and current limitations

Project conventions:

- Run commands from the repository root.
- Task status values are exactly `ToDo`, `InProgress`, and `Done`.
- Allowed transitions are `ToDo` to `InProgress`, `InProgress` to `Done`, and
  `Done` to `InProgress`.
- Task field validation belongs in `app/models.py`.
- Workflow transition rules belong in `app/business_rules.py`.
- Storage behavior belongs in `app/storage.py`.
- Tests use pytest and FastAPI's `TestClient`.

Current limitations:

- Tasks are stored in process memory and reset when the backend stops.
- There is no database or persistent storage.
- There is no authentication or permission model.
- The project has no deployment workflow and does not claim production
  readiness.
- Dependency versions are not pinned.
- CORS is configured only for `localhost:5500` and `127.0.0.1:5500`.
- The frontend is a single vanilla JavaScript HTML file.

## Technical decisions

Technical decisions are recorded in:

- [`docs/decisions/dockerfile-design.md`](docs/decisions/dockerfile-design.md)
  for the Module 4 container design.
- [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md) for the midcourse
  feature decisions.

Module 4 verification evidence is recorded in
[`docs/module4/verification.md`](docs/module4/verification.md), and the
three-tool reflection is recorded in
[`docs/module4/reflection.md`](docs/module4/reflection.md). Additional midcourse
workflow evidence is available under
[`docs/midcourse/`](docs/midcourse/).
