from fastapi import HTTPException, status

TASK_NOT_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователя не существует",
)
