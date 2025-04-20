from fastapi import APIRouter

from app.api.tasks.schemas import TaskResponse
from app.api.users import errors as user_errors
from app.core.depends import StoreDep
from app.core.utils import build_responses

router = APIRouter(prefix="/tasks", tags=["Задачки"])


@router.get(
    "",
    summary="Получить задачки по времени",
    response_description="Получить задачки в заданном диапазоне времени",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
)
async def get_tasks(
    store: StoreDep,
    start: str | None = None,
    end: str | None = None,
    event_id: int | None = None,
) -> list[TaskResponse]:
    res = await store.tasks_accessor.get_by_time(
        start=start,
        end=end,
        event_id=event_id,
    )
    return [TaskResponse.model_validate(elem) for elem in res]


@router.post(

)
async def create_task(

) -> int:
    return 201