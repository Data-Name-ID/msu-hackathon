import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.users.enums import UserType
from app.core.db import BaseModel
from app.core.models.mixins import IDMixin

if typing.TYPE_CHECKING:
    from app.api.notes.models import EventNoteModel


class GroupModel(IDMixin, BaseModel):
    __tablename__ = "groups"

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="group",
        cascade="all, delete",
        lazy="noload",
    )


class UserModel(IDMixin, BaseModel):
    __tablename__ = "users"

    type: Mapped[UserType]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(String(255))
    confirmed: Mapped[bool]

    group: Mapped["GroupModel"] = relationship(
        back_populates="users",
        lazy="noload",
    )
    event_notes: Mapped[list["EventNoteModel"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        lazy="noload",
    )
