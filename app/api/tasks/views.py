from http import HTTPStatus

from fastapi import APIRouter

from app.api.tasks.models import TaskModel
from app.api.tasks.schemas import Task, TaskComplete, TaskCompleteResponse, TaskNote
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


@router.put(
    "/{task_id:int}/note",
    summary="Добавить запись к задачке",
    response_description="Добавить запись к задачке",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
)
async def change_note(
    store: StoreDep,
    user: UserDep,
    task_id: int,
    task_note: TaskNote,
) -> TaskNote:
    res = await store.tasks_accessor.change_note(
        task_id=task_id,
        user_id=user.id,
        description=task_note.note,
        priority=task_note.priority,
    )

    return TaskNote(priority=res.priority, note=res.description)


@router.post(
    "/{task_id}/status",
    summary="Изменить статус задачи",
    response_description="Изменить статус выполнения статуса задачи",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
)
async def set_task_status(
    store: StoreDep,
    user: UserDep,
    task_id: int,
    task_complete: TaskComplete,
) -> TaskCompleteResponse | int:
    if task_complete.complete:
        return TaskCompleteResponse.model_validate(
            await store.tasks_accessor.create_task_complete(task_id, user.id),
        )
    await store.tasks_accessor.delete_task_complete(task_id, user.id)
    return HTTPStatus.NO_CONTENT
