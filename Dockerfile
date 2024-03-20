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
    git

RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version

WORKDIR /usr/local/src/hexlet-friends

COPY . .

RUN poetry install --extras psycopg2-binary --only main

FROM python:3.11-alpine as runner

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache libpq gettext

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /usr/local/src/hexlet-friends /usr/local/src/hexlet-friends
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN chown -R appuser:appgroup /usr/local/src/hexlet-friends

USER appuser

WORKDIR /usr/local/src/hexlet-friends

CMD /usr/local/src/hexlet-friends/docker-start.sh
