from pydantic import BaseModel

from app.api.users.enums import UserType


class FFToken(BaseModel):
    token: str


class UserPublic(BaseModel):
    id: int
    group_id: int | None
    confirmed: bool
    type: UserType


class UserConfirmed(BaseModel):
    id: int
    confirmed: bool


class UserID(BaseModel):
    user_id: int


class GroupNumber(BaseModel):
    group_number: str
