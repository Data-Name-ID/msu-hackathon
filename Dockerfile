FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /project

COPY ./uv.lock ./pyproject.toml ./
RUN uv sync --compile-bytecode --no-cache --no-dev
ENV PATH="/project/.venv/bin:$PATH"

COPY . .
CMD alembic upgrade head && fastapi run main.py --host 0.0.0.0 --port ${BACKEND__RUN__PORT}
