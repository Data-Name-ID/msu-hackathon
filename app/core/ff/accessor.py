from httpx import AsyncClient

from app.core.accessors import BaseAccessor
from app.core.ff.schemas import GroupData, GroupDataList, UserData


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

    @staticmethod
    async def get_groups_data() -> list[GroupData]:
        async with AsyncClient() as client:
            response = await client.get(
                url="https://api.profcomff.com/timetable/group/?limit=1000",
            )
            response.raise_for_status()
            return GroupDataList.model_validate(response.json()).items
