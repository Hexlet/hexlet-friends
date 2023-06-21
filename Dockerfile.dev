FROM python:3.11-alpine as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    curl \
    gettext \
    git \
    make 

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

WORKDIR /project/

COPY pyproject.toml poetry.lock ./

RUN poetry install --extras psycopg2-binary

WORKDIR /usr/local/src/hexlet-friends

CMD ["make", "start"]
