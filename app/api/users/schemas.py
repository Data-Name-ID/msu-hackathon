from pydantic import BaseModel, EmailStr


class FFToken(BaseModel):
    token: str


class UserData(BaseModel):
    id: int
    email: EmailStr | None
