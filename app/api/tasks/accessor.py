from datetime import UTC, datetime

from sqlalchemy import ColumnElement, Select, delete, exists, insert, select, update
from sqlalchemy.orm import joinedload, with_loader_criteria

from app.api.tasks.enums import TaskPriority
from app.api.tasks.models import TaskCompletesModel, TaskModel, TaskNotesModel
from app.api.tasks.schemas import TaskCreate
from app.api.users.models import UserModel
from app.core.accessors import BaseAccessor


class TaskAccessor(BaseAccessor):
    @staticmethod
    def _personal_filter(user: UserModel) -> ColumnElement[bool]:
        return TaskModel.author_id == user.id

    @staticmethod
    def _group_filter(user: UserModel) -> ColumnElement[bool]:
        return TaskModel.group_id == user.group_id

    def _access_filter(self, user: UserModel) -> ColumnElement[bool]:
        return self._personal_filter(user) | self._group_filter(user)

    def _base_stmt(self, user: UserModel) -> Select:
        return (
            select(TaskModel)
            .where(self._access_filter(user))
            .options(
                joinedload(TaskModel.completes),
                with_loader_criteria(
                    TaskCompletesModel,
                    TaskCompletesModel.user_id == user.id,
                ),
            )
        ).order_by(TaskModel.end_ts.asc())

    async def list_with_filters(
        self,
        user: UserModel,
        start: str | None = None,
        end: str | None = None,
        event_id: int | None = None,
    ) -> list[TaskModel]:
        stmt = self._base_stmt(user)

        if start is not None:
            start_date = datetime.strptime(start, "%Y-%m-%d").astimezone(UTC)
            stmt = stmt.where(TaskModel.start_ts >= start_date)
        if end is not None:
            end_date = datetime.strptime(end, "%Y-%m-%d").astimezone(UTC)
            stmt = stmt.where(TaskModel.end_ts <= end_date)

        if event_id is None:
            stmt = stmt.where(TaskModel.event_id == None)  # noqa: E711
        else:
            stmt = stmt.where(TaskModel.event_id == event_id)

        return (await self.store.db.scalars(stmt)).unique().all()

    async def get_by_id(self, user: UserModel, task_id: int) -> TaskModel | None:
        stmt = (
            self._base_stmt(user)
            .where(TaskModel.id == task_id)
            .options(
                joinedload(TaskModel.notes),
                joinedload(TaskModel.comments),
                with_loader_criteria(
                    TaskNotesModel,
                    TaskNotesModel.user_id == user.id,
                ),
            )
        )
        return await self.store.db.scalar(stmt)

    async def change_note(
        self,
        task_id: int,
        user_id: int,
        description: str | None,
        priority: TaskPriority,
    ) -> TaskNotesModel:
        stmt = select(
            exists(TaskNotesModel).where(
                TaskNotesModel.task_id == task_id,
                TaskNotesModel.user_id == user_id,
            ),
        )

        if not await self.store.db.scalar(stmt):
            stmt1 = insert(TaskNotesModel)
        else:
            stmt1 = update(TaskNotesModel)

        stmt1 = stmt1.values(
            task_id=task_id,
            user_id=user_id,
            description=description,
            priority=priority,
        ).returning(TaskNotesModel)

        return await self.store.db.scalar(stmt1)

    async def create_task_complete(
        self,
        task_id: int,
        user_id: int,
    ) -> TaskCompletesModel:
        stmt = select(TaskCompletesModel).where(
            TaskCompletesModel.task_id == task_id,
            TaskCompletesModel.user_id == user_id,
        )
        if (res := await self.store.db.scalar(stmt)) is not None:
            return res

        stmt = (
            insert(TaskCompletesModel)
            .values(
                task_id=task_id,
                user_id=user_id,
            )
            .returning(TaskCompletesModel)
        )
        return await self.store.db.scalar(stmt)

    async def delete_task_complete(self, task_id: int, user_id: int) -> None:
        stmt = delete(TaskCompletesModel).where(
            TaskCompletesModel.task_id == task_id,
            TaskCompletesModel.user_id == user_id,
        )
        await self.store.db.execute(stmt)

    async def create_task(self, task: TaskCreate, user: UserModel) -> TaskModel:
        stmt = (
            insert(TaskModel)
            .values(
                title=task.title,
                description=task.description,
                priority=task.priority,
                type=task.type,
                start_ts=task.start_ts,
                end_ts=task.end_ts,
                author_id=user.id,
                event_id=task.event_id,
                group_id=user.group_id if task.for_group else None,
            )
            .returning(TaskModel)
        )
        return await self.store.db.scalar(stmt)