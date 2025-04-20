from sqlalchemy import exists, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only

from app.api.users.models import GroupModel, UserModel
from app.core.accessors import BaseAccessor
from app.core.ff.schemas import GroupData, UserData


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

    async def get_students_by_group_id(self, group_id: int) -> list[UserModel]:
        stmt = (
            select(UserModel)
            .where(UserModel.group_id == group_id)
            .options(load_only(UserModel.id, UserModel.confirmed))
        )
        return (await self.store.db.scalars(stmt)).all()

    async def add_groups(self, groups: list[GroupData]) -> None:
        stmt = insert(GroupModel).values([group.model_dump() for group in groups])
        await self.store.db.execute(stmt)

    async def confirm_student(self, user_id: int) -> None:
        stmt = update(UserModel).where(UserModel.id == user_id).values(confirmed=True)
        await self.store.db.execute(stmt)

    async def get_group_id_by_number(self, group_number: str) -> int | None:
        stmt = select(GroupModel.id).where(GroupModel.number == group_number)
        return await self.store.db.scalar(stmt)

    async def set_group(self, *, user_id: int, group_id: int) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(group_id=group_id, confirmed=False)
        )
        await self.store.db.execute(stmt)
