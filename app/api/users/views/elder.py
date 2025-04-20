from fastapi import APIRouter

from app.api.users import errors
from app.api.users.enums import UserType
from app.api.users.models import UserModel
from app.api.users.schemas import UserConfirmed, UserID
from app.core.depends import StoreDep, UserDep
from app.core.schemas import MessageScheme
from app.core.utils import build_responses

router = APIRouter(prefix="/elder", tags=["Староста"])


@router.post(
    "/my_group",
    summary="Группа старосты",
    response_description="Список студентов группы старосты",
    responses=build_responses(errors.INVALID_TOKEN_ERROR),
    response_model=list[UserConfirmed],
)
async def my_group(
    user: UserDep,
    store: StoreDep,
) -> list[UserModel]:
    if user.type != UserType.ELDER.value:
        raise errors.USER_IS_NOT_ELDER_ERROR

    return await store.user_accessor.get_students_by_group_id(user.group_id)


@router.post(
    "/confirm",
    summary="Подтверждение студента",
    response_description="Студент подтвержден",
    responses=build_responses(errors.INVALID_TOKEN_ERROR),
)
async def confirm_student(
    user: UserDep,
    store: StoreDep,
    student: UserID,
) -> MessageScheme:
    if user.type != UserType.ELDER.value:
        raise errors.USER_IS_NOT_ELDER_ERROR

    await store.user_accessor.confirm_student(student.user_id)
    return MessageScheme(message="ok")
