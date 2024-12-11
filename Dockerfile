FROM python:3.11.5-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    UV_NO_SYNC=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /usr/local/src/hexlet-friends

COPY pyproject.toml uv.lock ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends make git

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN git config --global --add safe.directory "$(pwd)"
RUN uv sync
