from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Query,
    Path,
    Response,
)

from typing import List

from app.db.local_db import tasks_db, next_task_id

from app.schemas.task import (
    TaskCreate,
    TaskOut,
    TaskPatch,
    TaskUpdate,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={
        404: {"description": "Task not found"}
    },
)


# Raise 404 if the task does not exist.
def get_task_or_404(task_id: int) -> dict:
    task = tasks_db.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    return task


# GET /tasks
@router.get(
    "/",
    response_model=List[TaskOut],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
    description="Returns tasks",
)
def list_tasks(
    skip: int = Query(
        0,
        ge=0,
        description="Number of tasks to skip",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Limit number of tasks",
    ),
):
    results = list(tasks_db.values())

    return results[skip : skip + limit]


# GET /tasks/{task_id}
@router.get(
    "/{task_id}",
    response_model=TaskOut,
    summary="Get a single task",
)
def get_task(
    task_id: int = Path(
        ...,
        gt=0,
        description="The ID of the task",
    ),
):
    return get_task_or_404(task_id)


# POST /tasks
@router.post(
    "/",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        409: {"description": "This task already exists"}
    },
)
def create_task(task: TaskCreate):
    if any(
        item["text"].lower() == task.text.lower()
        for item in tasks_db.values()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task '{task.text}' already exists.",
        )

    task_id = next_task_id()

    new_task = {
        "id": task_id,
        **task.model_dump(),
    }

    tasks_db[task_id] = new_task

    return new_task


# PUT /tasks/{task_id}
@router.put(
    "/{task_id}",
    response_model=TaskOut,
    summary="Replace a task (full update)",
)
def replace_task(
    task_update: TaskUpdate,
    task_id: int = Path(
        ...,
        gt=0,
    ),
):
    get_task_or_404(task_id)

    updated = {
        "id": task_id,
        **task_update.model_dump(),
    }

    tasks_db[task_id] = updated

    return updated


# PATCH /tasks/{task_id}
@router.patch(
    "/{task_id}",
    response_model=TaskOut,
    summary="Partial update to task",
)
def patch_task(
    task_patch: TaskPatch,
    task_id: int = Path(
        ...,
        gt=0,
    ),
):
    existing = get_task_or_404(task_id)

    changes = task_patch.model_dump(
        exclude_unset=True
    )

    existing.update(changes)

    return existing


# DELETE /tasks/{task_id}
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    task_id: int = Path(
        ...,
        gt=0,
    ),
):
    get_task_or_404(task_id)

    del tasks_db[task_id]

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )