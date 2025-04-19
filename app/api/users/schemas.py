from pydantic import BaseModel, EmailStr

from app.api.users.enums import UserType


class FFToken(BaseModel):
    token: str


class UserData(BaseModel):
    id: int
    email: EmailStr | None


class UserPublic(BaseModel):
    id: int
    group_id: int | None
    confirmed: bool
    type: UserType
