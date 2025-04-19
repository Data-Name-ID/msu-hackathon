from httpx import AsyncClient

from app.api.users.schemas import UserData
from app.core.accessors import BaseAccessor


class FFAccessor(BaseAccessor):
    @staticmethod
    async def get_user_data(token: str) -> UserData:
        headers = {"Authorization": token}
        async with AsyncClient() as client:
            response = await client.get(
                url="https://api.profcomff.com/auth/me",
                headers=headers,
            )
            response.raise_for_status()
            return UserData.model_validate(response.json())
