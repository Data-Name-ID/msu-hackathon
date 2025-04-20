from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.users.models import UserModel
from app.core.store import Store

required_bearer = HTTPBearer()
optional_bearer = HTTPBearer(auto_error=False)

TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(required_bearer)]
OptionalTokenDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(optional_bearer),
]


def get_store(request: Request) -> Store:
    return request.app.state.store


StoreDep = Annotated[Store, Depends(get_store)]


async def user_dependency(token: TokenDep, store: StoreDep) -> UserModel:
    return await store.user_manager.fetch_user_from_access_token(token.credentials)


async def user_dependency_null_group(
    token: TokenDep,
    store: StoreDep,
) -> UserModel | None:
    user = await store.user_manager.fetch_user_from_access_token(token.credentials)
    if user.group_id is None:
        raise HTTPException(
            status_code=403,
            detail="Группа не установлена",
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=403,
            detail="Пользователь не подтвержден",
        )

    return user


UserDepCurrent = Annotated[UserModel, Depends(user_dependency)]
UserDep = Annotated[UserModel, Depends(user_dependency_null_group)]
