from fastapi import APIRouter
from httpx import HTTPStatusError

from app.api.users import errors
from app.api.users.enums import UserType
from app.core.depends import StoreDep, UserDep
from app.core.schemas import MessageScheme
from app.core.utils import build_responses

router = APIRouter(prefix="/admin", tags=["Администратор"])


@router.post(
    "/update_groups",
    summary="Обновление групп",
    response_description="Синхронизация списка групп с ФФ",
    responses=build_responses(errors.INVALID_TOKEN_ERROR),
)
async def update_groups(
    user: UserDep,
    store: StoreDep,
) -> MessageScheme:
    if user.type != UserType.ADMIN.value:
        raise errors.USER_IS_NOT_ADMIN_ERROR

    try:
        groups_data = await store.ff.get_groups_data()
    except HTTPStatusError as e:
        raise errors.FF_API_ERROR from e

    await store.user_accessor.add_groups(groups_data)
    return MessageScheme(message="ok")
