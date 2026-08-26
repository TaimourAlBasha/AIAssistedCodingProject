from datetime import date, datetime, timezone
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
    """Create a task response and store it in memory.

    Args:
        payload: The validated task creation fields.

    Returns:
        TaskResponse: The stored task with a UUID and UTC timestamps.
    """
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def is_task_overdue(task: TaskResponse, today: Optional[date] = None) -> bool:
    """Determine whether an incomplete task is past its due date.

    Args:
        task: The task to evaluate.
        today: An optional comparison date; defaults to the local current date.

    Returns:
        bool: ``True`` when the task has a past due date and is not done.
    """
    comparison_date = today or date.today()
    return (
        task.due_date is not None
        and task.due_date < comparison_date
        and task.status != TaskStatus.DONE
    )


def get_all_tasks(
    status=None,
    priority=None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    """Return stored tasks that match all supplied filters.

    Args:
        status: An optional value accepted by ``TaskStatus``.
        priority: An optional value accepted by ``TaskPriority``.
        overdue: An optional overdue-state filter.
        tag: An optional case-insensitive exact tag filter.

    Returns:
        list[TaskResponse]: Tasks matching every supplied filter.

    Raises:
        ValueError: If ``status`` or ``priority`` is not accepted by its enum.
    """
    tasks = list(_tasks.values())

    if status is not None:
        status = TaskStatus(status)
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        priority = TaskPriority(priority)
        tasks = [task for task in tasks if task.priority == priority]

    if overdue is not None:
        tasks = [task for task in tasks if is_task_overdue(task) is overdue]

    if tag is not None:
        comparison_tag = tag.strip().casefold()
        tasks = [
            task
            for task in tasks
            if any(task_tag.casefold() == comparison_tag for task_tag in task.tags)
        ]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a stored task by its identifier.

    Args:
        task_id: The task identifier to find.

    Returns:
        Optional[TaskResponse]: The matching task, or ``None`` if not found.
    """
    return _tasks.get(task_id)


def update_task(
    task_id: str,
    payload: TaskUpdate,
) -> Optional[TaskResponse]:
    """Apply explicitly supplied fields to a stored task.

    Args:
        task_id: The identifier of the task to update.
        payload: The validated partial update.

    Returns:
        Optional[TaskResponse]: The updated task, the unchanged task when no
        values differ, or ``None`` when the task does not exist.
    """
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
    """Delete a stored task by its identifier.

    Args:
        task_id: The identifier of the task to delete.

    Returns:
        bool: ``True`` if a task was removed, otherwise ``False``.
    """
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
