from typing import Annotated

from fastapi import APIRouter, Cookie, Request, Response
from httpx import HTTPStatusError

from app.api.users import errors
from app.api.users.models import UserModel
from app.api.users.schemas import FFToken, UserPublic
from app.core.depends import StoreDep, UserDepCurrent
from app.core.jwt.schemas import AccessToken, RefreshToken, TokenCollection
from app.core.utils import build_responses

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/signin",
    summary="Вход в систему",
    response_description="Коллекция токенов доступа",
    description="Устанавливает куку с refresh токеном.",
    responses=build_responses(errors.INVALID_TOKEN_ERROR),
)
async def sign_in(
    data: FFToken,
    request: Request,
    response: Response,
    store: StoreDep,
) -> TokenCollection:
    try:
        user_data = await store.ff.get_user_data(data.token)
    except HTTPStatusError as e:
        raise errors.INVALID_TOKEN_ERROR from e

    if not await store.user_accessor.exists_by_id(user_data.id):
        await store.user_accessor.create(user_data)

    token_collection = store.jwt.create_token_collection(user_data.id)
    store.user_manager.set_refresh_token_cookie(
        request=request,
        response=response,
        token=token_collection.refresh_token,
    )
    return token_collection


@router.get(
    "/current",
    summary="Текущий пользователь",
    response_description="Текущий пользователь",
    response_model=UserPublic,
    responses=build_responses(
        errors.INVALID_TOKEN_ERROR,
        errors.USER_NOT_EXISTS_ERROR,
    ),
)
async def current_user(user: UserDepCurrent) -> UserModel:
    return user


@router.post(
    "/refresh",
    summary="Обновление токена",
    description="Использует refresh токен из куки либо из тела запроса.",
    response_description="Токен доступа",
    responses=build_responses(
        errors.INVALID_TOKEN_ERROR,
        errors.USER_NOT_EXISTS_ERROR,
    ),
)
async def refresh(
    store: StoreDep,
    credentials: RefreshToken | None = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> AccessToken:
    token = credentials.refresh_token if credentials is not None else refresh_token

    if token is not None:
        return await store.user_manager.refresh_access_token(token)

    raise errors.REFRESH_TOKEN_NOT_PROVIDED_ERROR
