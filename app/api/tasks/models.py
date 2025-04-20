from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.tasks.enums import TaskPriority, TaskType
from app.core.db import BaseModel
from app.core.models.mixins import IDMixin


class TaskModel(IDMixin, BaseModel):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[TaskPriority]
    type: Mapped[TaskType]
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int | None] = mapped_column(nullable=True)
    start_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    attachments: Mapped[list["TaskAttachmentModel"]] = relationship(
        back_populates="task",
        cascade="all, delete",
        lazy="noload",
    )
    notes: Mapped[list["TaskNotesModel"]] = relationship(
        back_populates="task",
        cascade="all, delete",
        lazy="noload",
    )
    completes: Mapped[list["TaskCompletesModel"]] = relationship(
        back_populates="task",
        cascade="all, delete",
        lazy="noload",
    )
    comments: Mapped[list["TaskCommentsModel"]] = relationship(
        back_populates="task",
        cascade="all, delete",
        lazy="noload",
    )


class TaskAttachmentModel(IDMixin, BaseModel):
    __tablename__ = "task_attachments"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(2048))

    task: Mapped["TaskModel"] = relationship(
        back_populates="attachments",
        lazy="noload",
    )


class TaskNotesModel(BaseModel):
    __tablename__ = "task_notes"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[TaskPriority]

    task: Mapped["TaskModel"] = relationship(back_populates="notes", lazy="noload")


class TaskCompletesModel(IDMixin, BaseModel):
    __tablename__ = "task_completes"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    task: Mapped["TaskModel"] = relationship(back_populates="completes", lazy="noload")


class TaskCommentsModel(IDMixin, BaseModel):
    __tablename__ = "task_comments"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str]

    task: Mapped["TaskModel"] = relationship(back_populates="comments", lazy="noload")
