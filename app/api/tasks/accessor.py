from datetime import UTC, datetime

from sqlalchemy import select

from app.api.tasks.models import TaskModel
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
