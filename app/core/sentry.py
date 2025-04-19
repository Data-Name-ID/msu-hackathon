import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


def init_sentry(*, dsn: str, environment: str) -> None:
    sentry_sdk.init(
        dsn=dsn,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
        integrations=[
            FastApiIntegration(),
            LoggingIntegration(),
            SqlalchemyIntegration(),
        ],
        environment=environment,
    )
