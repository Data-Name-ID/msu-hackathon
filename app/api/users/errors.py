from fastapi import HTTPException, status

INVALID_TOKEN_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Недействительный токен",
)
REFRESH_TOKEN_NOT_PROVIDED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh токен не был предоставлен",
)
USER_IS_NOT_ELDER_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь не является старостой",
)
USER_IS_NOT_ADMIN_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь не является администратором",
)
USER_NOT_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователя не существует",
)
FF_API_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка при обращении к API ФФ",
)
GROUP_NOT_EXISTS_ERROR = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Группа не существует",
)
