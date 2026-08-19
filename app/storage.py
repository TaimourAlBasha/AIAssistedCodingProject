from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(status=None, priority=None) -> list[TaskResponse]:
    tasks = list(_tasks.values())

    if status is not None:
        status = TaskStatus(status)
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        priority = TaskPriority(priority)
        tasks = [task for task in tasks if task.priority == priority]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(
    task_id: str,
    payload: TaskUpdate,
) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if "description" in updates and updates["description"] is None:
        updates["description"] = ""

    changed = any(getattr(task, field) != value for field, value in updates.items())
    if not changed:
        return task

    updates["updated_at"] = datetime.now(timezone.utc)
    updated_task = task.model_copy(update=updates)
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
