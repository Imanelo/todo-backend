from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.models import Task, TaskCreate, TaskUpdate
from app.storage import task_storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Add a new task to the task tracker.",
)
def create_task(task_in: TaskCreate) -> Task:
    return task_storage.add(task_in)


@router.get(
    "",
    response_model=list[Task],
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description="Retrieve all tasks, optionally filtering by completion status.",
)
def list_tasks(
    completed: Optional[bool] = Query(
        default=None,
        description="Filter tasks by completion status (true/false)",
    ),
) -> list[Task]:
    return task_storage.list(completed=completed)


@router.get(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Retrieve a single task by its unique ID.",
)
def get_task(task_id: int) -> Task:
    task = task_storage.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Update a task (PUT)",
    description="Update fields of an existing task.",
)
def update_task_put(task_id: int, task_update: TaskUpdate) -> Task:
    updated = task_storage.update(task_id, task_update)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return updated


@router.patch(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Partially update a task (PATCH)",
    description="Partially update fields of an existing task.",
)
def update_task_patch(task_id: int, task_update: TaskUpdate) -> Task:
    updated = task_storage.update(task_id, task_update)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return updated


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Remove a task from the tracker.",
)
def delete_task(task_id: int) -> None:
    deleted = task_storage.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

