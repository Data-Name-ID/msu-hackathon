from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    id: int
    email: EmailStr | None


class GroupData(BaseModel):
    id: int
    number: str


class GroupDataList(BaseModel):
    items: list[GroupData]
