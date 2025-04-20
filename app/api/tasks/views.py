from fastapi import APIRouter

from app.api.tasks import errors as task_errors
from app.api.tasks.models import TaskModel
from app.api.tasks.schemas import Task
from app.api.users import errors as user_errors
from app.core.depends import StoreDep, UserDep
from app.core.utils import build_responses

router = APIRouter(prefix="/tasks", tags=["Задачки"])


@router.get(
    "",
    summary="Получить задачи по времени",
    response_description="Получить задачи в заданном диапазоне времени",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
    response_model=list[Task],
)
async def get_tasks(
    user: UserDep,
    store: StoreDep,
    start: str | None = None,
    end: str | None = None,
    event_id: int | None = None,
) -> list[TaskModel]:
    return await store.tasks_accessor.list_with_filters(
        start=start,
        end=end,
        event_id=event_id,
        user=user,
    )


@router.get(
    "/{task_id}",
    summary="Получить задачу по ID",
    response_description="Получить задачу по ID",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
    response_model=Task,
)
async def get_task(
    user: UserDep,
    store: StoreDep,
    task_id: int,
) -> TaskModel:
    task = await store.tasks_accessor.get_by_id(task_id=task_id, user=user)

    if task is None:
        raise task_errors.TASK_NOT_EXISTS_ERROR

    return task
