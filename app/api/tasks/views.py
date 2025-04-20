from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import APIRouter

from app.api.tasks import errors as task_errors
from app.api.tasks.models import TaskModel
from app.api.tasks.schemas import (
    GeminiAnswer,
    GeminiQuestion,
    Task,
    TaskComplete,
    TaskCompleteResponse,
    TaskCreate,
    TaskNote,
    TaskPublic,
)
from app.api.users import errors as user_errors
from app.api.users.enums import UserType
from app.core.depends import StoreDep, UserDep
from app.core.utils import build_responses

router = APIRouter(prefix="/tasks", tags=["Задачки"])


@router.get(
    "",
    summary="Получить задачи по времени",
    response_description="Получить задачи в заданном диапазоне времени",
    responses=build_responses(
        user_errors.INVALID_TOKEN_ERROR,
    ),
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
    response_model=TaskPublic,
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


@router.delete(
    "/{task_id}",
    summary="Получить задачу по ID",
    response_description="Получить задачу по ID",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
)
async def delete_task(
    user: UserDep,
    store: StoreDep,
    task_id: int,
) -> int:
    await store.tasks_accessor.delete_by_id(task_id=task_id, user_id=user.id)
    return HTTPStatus.NO_CONTENT


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
    "",
    summary="Создание задачи",
    response_description="Создание задачи",
    responses=build_responses(user_errors.INVALID_TOKEN_ERROR),
    response_model=Task,
)
async def create_task(store: StoreDep, user: UserDep, task: TaskCreate) -> TaskModel:
    if user.type != UserType.ELDER and task.for_group:
        raise user_errors.USER_IS_NOT_ELDER_ERROR
    return await store.tasks_accessor.create_task(task=task, user=user)


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


@router.post("/ai")
async def ai_task(
    store: StoreDep,
    user: UserDep,
    question: GeminiQuestion,
) -> GeminiAnswer:
    start_ts = (datetime.now()).strftime("%Y-%m-%d")
    end_ts = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    schedule_json_string = await store.ff.get_events_data(
        start_ts,
        end_ts,
        user.group_id,
    )
    tasks_json_string = [
        TaskPublic.model_validate(task).model_dump()
        for task in await store.tasks_accessor.list_with_filters(
            start=start_ts,
            end=end_ts,
            user=user,
        )
    ]

    return GeminiAnswer(
        answer=await store.gemini.get_answer(
            schedule_context=schedule_json_string,
            tasks_context=tasks_json_string,
            question=question.question,
        ),
    )
