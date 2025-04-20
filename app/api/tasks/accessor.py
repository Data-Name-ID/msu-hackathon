from datetime import UTC, datetime

from sqlalchemy import delete, exists, insert, select, update

from app.api.tasks.enums import TaskPriority
from app.api.tasks.models import TaskCompletesModel, TaskModel, TaskNotesModel
from app.core.accessors import BaseAccessor


class TaskAccessor(BaseAccessor):
    async def list_with_filters(
        self,
        start: str | None = None,
        end: str | None = None,
        event_id: int | None = None,
    ) -> list[TaskModel]:
        stmt = select(TaskModel)

        if start is not None:
            start_date = datetime.strptime(start, "%Y-%m-%d").astimezone(UTC)
            stmt = stmt.where(TaskModel.start_ts <= start_date)
        if end is not None:
            end_date = datetime.strptime(end, "%Y-%m-%d").astimezone(UTC)
            stmt = stmt.where(TaskModel.end_ts <= end_date)

        if event_id is None:
            stmt = stmt.where(TaskModel.event_id is None)
        else:
            stmt = stmt.where(TaskModel.event_id == event_id)

        return self.store.db.scalars(stmt)

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
