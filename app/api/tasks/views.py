from fastapi import APIRouter

from app.api.tasks.models import TaskModel
from app.api.tasks.schemas import Task
from app.api.users import errors as user_errors
from app.core.depends import StoreDep
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
    store: StoreDep,
    start: str | None = None,
    end: str | None = None,
    event_id: int | None = None,
) -> list[TaskModel]:
    return await store.tasks_accessor.list_with_filters(
        start=start,
        end=end,
        event_id=event_id,
    )
