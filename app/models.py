from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the task")
    description: Optional[str] = Field(default=None, max_length=1000, description="Detailed description of the task")
    completed: bool = Field(default=False, description="Whether the task has been completed")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty or whitespace only")
        return trimmed


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Updated title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Updated description")
    completed: Optional[bool] = Field(default=None, description="Updated completion status")

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Title cannot be empty or whitespace only")
        return trimmed


class Task(TaskBase):
    id: int = Field(..., description="Unique identifier for the task")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when created")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when last updated")

