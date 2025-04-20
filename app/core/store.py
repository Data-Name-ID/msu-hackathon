import logging


class Store:
    def __init__(self) -> None:
        from app.core.config import Config

        self.config = Config()
        self.logger = logging.getLogger("msu.store")

        from app.core.db import DatabaseAccessor
        from app.core.email import EmailManager
        from app.core.ff.accessor import FFAccessor
        from app.core.gemini import GeminiAccessor
        from app.core.jwt import JWTManager
        from app.core.s3 import S3Accessor

        self.db = DatabaseAccessor(self)
        self.email = EmailManager(self)
        self.ff = FFAccessor(self)
        self.jwt = JWTManager(self)
        self.s3 = S3Accessor(self)
        self.gemini = GeminiAccessor(self)

        from app.api.users.accessor import UserAccessor

        self.user_accessor = UserAccessor(self)

        from app.api.users.manager import UserManager

        self.user_manager = UserManager(self)

        from app.api.tasks.accessor import TaskAccessor

        self.tasks_accessor = TaskAccessor(self)
