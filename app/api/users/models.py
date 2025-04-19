from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.notes.models import EventNoteModel
from app.api.users.enums import UserType
from app.core.db import BaseModel
from app.core.models.mixins import IDMixin


class GroupModel(IDMixin, BaseModel):
    __tablename__ = "groups"

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="group",
        cascade="all, delete",
        lazy="noload",
    )


class UserModel(IDMixin, BaseModel):
    __tablename__ = "users"

    type: Mapped[UserType] = mapped_column(default=UserType.STUDENT)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(default=False)

    group: Mapped["GroupModel"] = relationship(
        back_populates="users",
        lazy="noload",
    )
    event_notes: Mapped[list[EventNoteModel]] = relationship(
        back_populates="user",
        cascade="all, delete",
        lazy="noload",
    )
