import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import BaseModel
from app.core.models.mixins import IDMixin

if typing.TYPE_CHECKING:
    from app.api.users.models import UserModel


class EventNoteModel(IDMixin, BaseModel):
    __tablename__ = "event_notes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int]
    text: Mapped[str]

    user: Mapped["UserModel"] = relationship(
        back_populates="event_notes",
        lazy="noload",
    )
