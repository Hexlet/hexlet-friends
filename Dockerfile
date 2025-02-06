FROM python:3.11.5-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    UV_NO_SYNC=1 \
    UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends make git
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV VIRTUAL_ENV=/opt/venv

RUN uv venv $VIRTUAL_ENV --python 3.13

ENV UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV

WORKDIR /usr/local/src/hexlet-friends

RUN git config --global --add safe.directory "$(pwd)"

COPY pyproject.toml ./

RUN uv sync
