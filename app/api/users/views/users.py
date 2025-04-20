from fastapi import APIRouter

from app.api.users import errors
from app.api.users.schemas import GroupNumber
from app.core.depends import StoreDep, UserDep
from app.core.schemas import MessageScheme
from app.core.utils import build_responses

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/set_group",
    summary="Установка группы",
    response_description="Установлена группа",
    responses=build_responses(errors.INVALID_TOKEN_ERROR),
)
async def set_group(
    user: UserDep,
    store: StoreDep,
    group: GroupNumber,
) -> MessageScheme:
    group_id = await store.user_accessor.get_group_id_by_number(group.group_number)

    if group_id is None:
        raise errors.GROUP_NOT_EXISTS_ERROR

    await store.user_accessor.set_group(user_id=user.id, group_id=group_id)
    return MessageScheme(message="ok")
