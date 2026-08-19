import unittest

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.storage import (
    _reset,
    add_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        _reset()

    def tearDown(self) -> None:
        _reset()

    def test_add_and_get_task(self) -> None:
        task = add_task(TaskCreate(title="Create API"))

        self.assertEqual(get_task_by_id(task.id), task)
        self.assertEqual(get_all_tasks(), [task])
        self.assertEqual(task.created_at, task.updated_at)

    def test_get_missing_task_returns_none(self) -> None:
        self.assertIsNone(get_task_by_id("missing"))

    def test_filter_tasks_by_status_and_priority(self) -> None:
        todo_high = add_task(
            TaskCreate(
                title="Urgent task",
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
            )
        )
        add_task(
            TaskCreate(
                title="Completed task",
                status=TaskStatus.DONE,
                priority=TaskPriority.LOW,
            )
        )

        self.assertEqual(get_all_tasks(status=TaskStatus.TODO), [todo_high])
        self.assertEqual(get_all_tasks(priority=TaskPriority.HIGH), [todo_high])
        self.assertEqual(
            get_all_tasks(
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
            ),
            [todo_high],
        )

    def test_update_only_changes_provided_fields(self) -> None:
        original = add_task(
            TaskCreate(
                title="Original",
                description="Keep this",
                priority=TaskPriority.LOW,
            )
        )

        updated = update_task(
            original.id,
            TaskUpdate(title="Updated", status=TaskStatus.IN_PROGRESS),
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Updated")
        self.assertEqual(updated.description, "Keep this")
        self.assertEqual(updated.priority, TaskPriority.LOW)
        self.assertEqual(updated.status, TaskStatus.IN_PROGRESS)
        self.assertEqual(updated.created_at, original.created_at)
        self.assertGreaterEqual(updated.updated_at, original.updated_at)

    def test_update_missing_task_returns_none(self) -> None:
        result = update_task("missing", TaskUpdate(title="Updated"))

        self.assertIsNone(result)

    def test_delete_task(self) -> None:
        task = add_task(TaskCreate(title="Delete me"))

        self.assertTrue(delete_task(task.id))
        self.assertIsNone(get_task_by_id(task.id))
        self.assertFalse(delete_task(task.id))

    def test_reset_clears_all_tasks(self) -> None:
        add_task(TaskCreate(title="Temporary"))

        _reset()

        self.assertEqual(get_all_tasks(), [])


if __name__ == "__main__":
    unittest.main()
