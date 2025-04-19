from sqlalchemy import exists, select, update
from sqlalchemy.dialects.postgresql import insert

from app.api.users.models import UserModel
from app.api.users.schemas import UserData
from app.core.accessors import BaseAccessor


class UserAccessor(BaseAccessor):
    async def create(self, user_in: UserData) -> None:
        stmt = insert(UserModel).values(**user_in.model_dump())
        await self.store.db.execute(stmt)

    async def exists_by_id(self, user_id: int) -> bool:
        stmt = select(exists().where(UserModel.id == user_id))
        return await self.store.db.scalar(stmt)

    async def fetch_by_id(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        return await self.store.db.scalar(stmt)

    async def confirm(self, user_id: int) -> None:
        stmt = update(UserModel).where(UserModel.id == user_id).values(confirmed=True)
        await self.store.db.execute(stmt)
