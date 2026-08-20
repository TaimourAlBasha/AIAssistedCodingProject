from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


MAX_TAGS = 5
MAX_TAG_LENGTH = 30


def normalize_tags(value: Optional[list[str]]) -> list[str]:
    normalized_tags: list[str] = []
    seen: set[str] = set()

    for tag in value or []:
        normalized = tag.strip()
        if not normalized:
            raise ValueError("tags must not contain blank values")
        if len(normalized) > MAX_TAG_LENGTH:
            raise ValueError(f"tags must not exceed {MAX_TAG_LENGTH} characters")

        comparison_key = normalized.casefold()
        if comparison_key not in seen:
            seen.add(comparison_key)
            normalized_tags.append(normalized)

    if len(normalized_tags) > MAX_TAGS:
        raise ValueError(f"tasks must not have more than {MAX_TAGS} tags")

    return normalized_tags


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        if len(value) > 200:
            raise ValueError("title must not exceed 200 characters")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return normalize_tags(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        if len(value) > 200:
            raise ValueError("title must not exceed 200 characters")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: Optional[list[str]]) -> list[str]:
        return normalize_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
