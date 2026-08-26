from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskResponse, TaskUpdate

load_dotenv()

FRONTEND_FILE = Path(__file__).resolve().parent.parent / "frontend" / "index.html"

app = FastAPI(
    title="Task Tracker API",
    description="Module 4 learning project API for a simple shared task tracker.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def task_board() -> FileResponse:
    """Serve the Task Tracker frontend.

    Returns:
        FileResponse: The response containing ``frontend/index.html``.

    Example:
        Request ``GET /``.
    """
    return FileResponse(FRONTEND_FILE)

@app.get("/health")
def health_check() -> dict[str, str]:
    """Report that the API process is running.

    Returns:
        dict[str, str]: A status value and the current UTC timestamp in ISO
        format.

    Example:
        Request ``GET /health``.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/version")
def get_version() -> dict[str, str]:
    """Return the FastAPI application's configured version.

    Returns:
        dict[str, str]: A mapping containing ``app.version``.

    Example:
        Request ``GET /version``.
    """
    return {"version": app.version}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a task.

    Args:
        payload: The validated fields for the new task.

    Returns:
        TaskResponse: The stored task, including its generated identifier and
        timestamps.

    Example:
        Send ``POST /tasks`` with ``{"title": "Write tests"}``.
    """
    return storage.add_task(payload)


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["tasks"],
)
def list_tasks(
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtering by overdue state and tag.

    Args:
        overdue: When provided, select tasks matching that overdue state.
        tag: When provided, select tasks containing that tag.

    Returns:
        list[TaskResponse]: The tasks matching all supplied filters.

    Raises:
        HTTPException: If ``tag`` is present but blank after trimming.

    Example:
        Request ``GET /tasks?overdue=true&tag=backend``.
    """
    if tag is not None and not tag.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tag filter must not be blank",
        )

    return storage.get_all_tasks(overdue=overdue, tag=tag)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def get_task(task_id: str) -> TaskResponse:
    """Return one task by its identifier.

    Args:
        task_id: The task identifier to retrieve.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: If no task has the supplied identifier.

    Example:
        Request ``GET /tasks/{task_id}``.
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def update_task_route(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Apply a partial update to an existing task.

    Args:
        task_id: The identifier of the task to update.
        payload: The validated fields included in the partial update.

    Returns:
        TaskResponse: The task after applying the supplied fields.

    Raises:
        HTTPException: If the task does not exist or a supplied status change
            violates the configured transition rules.

    Example:
        Send ``PATCH /tasks/{task_id}`` with ``{"status": "InProgress"}``.
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        validate_status_transition(existing.status, payload.status)

    updated_task = storage.update_task(task_id, payload)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task_route(task_id: str) -> None:
    """Delete a task by its identifier.

    Args:
        task_id: The identifier of the task to delete.

    Returns:
        None.

    Raises:
        HTTPException: If no task has the supplied identifier.

    Example:
        Request ``DELETE /tasks/{task_id}``.
    """
    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
