from httpx import AsyncClient

from app.api.tasks.schemas import TaskPublic
from app.core.accessors import BaseAccessor


class GeminiAccessor(BaseAccessor):
    async def request(
        self,
        tasks_context: list[TaskPublic],
    ) -> dict:
        async with AsyncClient() as client:
            response = await client.post(
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=AIzaSyB0VQ5M3LiWySNAiAD5Dxtp2qZiJEGQpNw",
                data={"contents": [{"parts": [{"text": ""}]}]},
            )
            response.raise_for_status()
            return response.json()
