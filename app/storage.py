import threading
from datetime import datetime, timezone
from typing import Optional
from app.models import Task, TaskCreate, TaskUpdate


class TaskStorage:
    """Thread-safe in-memory storage for tasks."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._current_id: int = 0
        self._lock = threading.Lock()

    def add(self, task_in: TaskCreate) -> Task:
        with self._lock:
            self._current_id += 1
            now = datetime.now(timezone.utc)
            task = Task(
                id=self._current_id,
                title=task_in.title,
                description=task_in.description,
                completed=task_in.completed,
                created_at=now,
                updated_at=now,
            )
            self._tasks[task.id] = task
            return task

    def get(self, task_id: int) -> Optional[Task]:
        with self._lock:
            return self._tasks.get(task_id)

    def list(self, completed: Optional[bool] = None) -> list[Task]:
        with self._lock:
            tasks = list(self._tasks.values())
            if completed is not None:
                tasks = [t for t in tasks if t.completed is completed]
            return tasks

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        with self._lock:
            existing = self._tasks.get(task_id)
            if existing is None:
                return None

            update_data = task_update.model_dump(exclude_unset=True)
            if not update_data:
                return existing

            updated_task = existing.model_copy(
                update={
                    **update_data,
                    "updated_at": datetime.now(timezone.utc),
                }
            )
            self._tasks[task_id] = updated_task
            return updated_task

    def delete(self, task_id: int) -> bool:
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._current_id = 0


# Global storage instance
task_storage = TaskStorage()

