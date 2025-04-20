import datetime
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from app.api.tasks.enums import TaskPriority, TaskType
from app.api.tasks.models import TaskCompletesModel, TaskNotesModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    task_id: int


class CommentPublic(CommentBase):
    id: int


class TaskBase(BaseModel):
    title: str
    priority: TaskPriority = TaskPriority.NORMAL
    type: TaskType = TaskType.GENERAL
    date: datetime.date | None = None
    event_id: int | None = None

    model_config = ConfigDict(populate_by_name=True)


class TaskCreate(TaskBase):
    description: str | None = None
    start_ts: datetime.datetime | None = None
    end_ts: datetime.datetime | None = None
    for_group: bool

    @model_validator(mode="before")
    @staticmethod
    def adjust_dates(data: dict[str, Any]) -> dict[str, Any]:
        if data.get("date"):
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
            data["start_ts"] = datetime.datetime.combine(date, datetime.time.min)
            data["end_ts"] = datetime.datetime.combine(date, datetime.time.max)

        return data


class Task(TaskBase):
    id: int
    completes: bool = Field(alias="completed")
    start_ts: datetime.datetime | None
    end_ts: datetime.datetime | None
    group_id: bool = Field(alias="for_group")

    @model_validator(mode="before")
    def adjust_dates(self) -> Self:
        if self.start_ts is None or self.end_ts is None:
            msg = "Start and end timestamps cannot be None."
            raise ValueError(msg)

        if (
            self.start_ts.time() == datetime.time.min
            and self.end_ts.time() == datetime.time.max
        ):
            self.date = self.start_ts.date()
            self.start_ts = None
            self.end_ts = None

        return self

    @field_validator("completes", mode="before")
    @classmethod
    def q(cls, completes: list[TaskCompletesModel]) -> bool:
        return completes != []

    @field_validator("group_id", mode="before")
    @classmethod
    def qq(cls, group_id: int | None) -> bool:
        return group_id is not None


class TaskPublic(Task):
    description: str | None = None
    notes: str | None = Field(default=None, alias="note")
    comments: list[CommentPublic] | None = None

    @field_validator("notes", mode="before")
    @classmethod
    def note_to_description(
        cls,
        notes: list[TaskNotesModel],
        info: ValidationInfo,
    ) -> str | None:
        if len(notes) != 0:
            info.data["priority"] = notes[0].priority
            return notes[0].description

        return None


class TaskUpdate(TaskBase):
    id: int
    description: str | None = None
    start_ts: datetime.datetime | None = None
    end_ts: datetime.datetime | None = None

    @model_validator(mode="before")
    def adjust_dates(self) -> "TaskUpdate":
        if self.date:
            self.start_ts = datetime.datetime.combine(self.date, datetime.time.min)
            self.end_ts = datetime.datetime.combine(self.date, datetime.time.max)

        return self


class TaskNote(BaseModel):
    priority: TaskPriority = TaskPriority.NORMAL
    note: str | None = None


class TaskComplete(BaseModel):
    complete: bool


class TaskCompleteResponse(BaseModel):
    task_id: int
    user_id: int

    class Config:
        from_attributes = True


class GeminiQuestion(BaseModel):
    question: str


class GeminiAnswer(BaseModel):
    answer: str
