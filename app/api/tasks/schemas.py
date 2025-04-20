import datetime

from pydantic import BaseModel, model_validator

from app.api.tasks.enums import TaskPriority, TaskType


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
    start_ts: datetime.datetime | None = None
    end_ts: datetime.datetime | None = None
    completed: bool
    for_group: bool


class TaskCreate(TaskBase):
    description: str | None = None
    event_id: int | None = None

    @model_validator(mode="before")
    def adjust_dates(self) -> "TaskCreate":
        if self.date:
            self.start_ts = datetime.datetime.combine(self.date, datetime.time.min)
            self.end_ts = datetime.datetime.combine(self.date, datetime.time.max)

        return self


class Task(TaskBase):
    @model_validator(mode="before")
    def adjust_dates(self) -> "Task":
        if (
            self.start_ts.time() == datetime.time.min
            and self.end_ts.time() == datetime.time.max
        ):
            self.date = self.start_ts.date()
            self.start_ts = None
            self.end_ts = None


class TaskPublic(TaskBase):
    id: int
    event_id: int | None = None
    description: str | None = None
    note: str | None = None
    comments: list[CommentPublic] | None = None


class TaskUpdate(TaskBase):
    id: int
    description: str | None = None
    event_id: int | None = None

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
