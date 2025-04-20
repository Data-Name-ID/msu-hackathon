from datetime import datetime

from pydantic import BaseModel, model_validator

from app.api.tasks.enums import TaskPriority, TaskType


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.NORMAL
    type: TaskType = TaskType.GENERAL
    event_id: int | None = None
    date: datetime | None = None
    start_ts: datetime | None = None
    end_ts: datetime | None = None
    for_group: bool
    note: str

    @model_validator(mode="before")
    @classmethod
    def adjust_dates(cls, data: dict):
        start = data.get("start_ts")
        end = data.get("end_ts")
        date_val = data.get("date")

        if start and end and start == end:
            data["date"] = start.date()
            data["start_ts"] = None
            data["end_ts"] = None

        elif date_val and not start and not end:
            dt = datetime.combine(date_val, datetime.min.time())
            data["start_ts"] = dt
            data["end_ts"] = dt

        return data


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: TaskPriority
    type: TaskType
    date: datetime | None
    start_ts: datetime | None
    end_ts: datetime | None

    @model_validator(mode="before")
    @classmethod
    def adjust_dates(cls, values: dict) -> dict:
        start = values.get("start_ts")
        end = values.get("end_ts")
        date = values.get("date")

        if start and end and start == end:
            values["date"] = start
            values["start_ts"] = None
            values["end_ts"] = None

        elif date and not start and not end:
            values["start_ts"] = date
            values["end_ts"] = date

        return values

    class Config:
        from_attributes = True
