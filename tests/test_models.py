import unittest

from pydantic import ValidationError

from app.models import (
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


class TaskCreateTests(unittest.TestCase):
    def test_defaults_and_title_stripping(self) -> None:
        task = TaskCreate(title="  Write tests  ")

        self.assertEqual(task.title, "Write tests")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertIsNone(task.assignee)

    def test_blank_title_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskCreate(title="   ")

    def test_title_over_200_characters_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskCreate(title="x" * 201)

    def test_extra_fields_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskCreate(title="Valid", unexpected="value")

    def test_more_than_five_tags_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskCreate(title="Too many tags", tags=[f"tag-{index}" for index in range(6)])

    def test_tags_over_thirty_characters_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskCreate(title="Long tag", tags=["x" * 31])


class TaskUpdateTests(unittest.TestCase):
    def test_all_fields_are_optional(self) -> None:
        update = TaskUpdate()

        self.assertEqual(update.model_dump(exclude_unset=True), {})

    def test_provided_title_is_stripped(self) -> None:
        update = TaskUpdate(title="  Updated title  ")

        self.assertEqual(update.title, "Updated title")

    def test_blank_provided_title_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskUpdate(title="   ")

    def test_extra_fields_are_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            TaskUpdate(id="not-editable")


if __name__ == "__main__":
    unittest.main()
