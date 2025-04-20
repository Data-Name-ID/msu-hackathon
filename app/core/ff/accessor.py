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
                timeout=1000,
            )
            response.raise_for_status()
            return UserData.model_validate(response.json())

    @staticmethod
    async def get_groups_data() -> list[GroupData]:
        async with AsyncClient() as client:
            response = await client.get(
                url="https://api.profcomff.com/timetable/group/?limit=1000",
                timeout=1000,
            )
            response.raise_for_status()
            return GroupDataList.model_validate(response.json()).items

    @staticmethod
    async def get_events_data(start_ts: str, end_ts: str, group_id: int) -> dict:
        async with AsyncClient() as client:
            response = await client.get(
                url="https://api.profcomff.com/timetable/event/",
                params={
                    "start": start_ts,
                    "end": end_ts,
                    "group_id": group_id,
                    "limit": 1000,
                },
                timeout=1000,
            )
            response.raise_for_status()
            return response.json()
