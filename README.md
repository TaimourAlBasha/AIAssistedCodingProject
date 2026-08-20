# Task Tracker

A small FastAPI and vanilla-JavaScript Kanban task tracker. Tasks are stored in memory and reset whenever the backend process stops.

## Install

Create or activate a Python virtual environment, then install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

From the project root:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Open <http://127.0.0.1:8000/>. The backend serves the frontend directly. API documentation is available at <http://127.0.0.1:8000/docs>.

## Test

Run the complete suite:

```powershell
python -m pytest -q
```

## Midcourse features

### Due dates

- Optional ISO calendar dates on create and update
- Date clearing through PATCH with `null`
- Accessible overdue indication for incomplete tasks due before today
- `GET /tasks?overdue=true` filtering
- Compact overdue filter on the board

### Tags

- Up to 5 tags of 30 characters each
- Whitespace normalization and blank-value rejection
- Case-insensitive deduplication and filtering
- Tag editing and card chips
- `GET /tasks?tag=backend` filtering
- Combined filtering with `GET /tasks?overdue=true&tag=backend`

Project workflow evidence and design notes are under [`docs/midcourse/`](docs/midcourse/).
