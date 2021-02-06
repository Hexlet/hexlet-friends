FROM python:3.8-alpine

ARG DJANGO_ENV

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=false \
    POETRY_VERSION=1.1.4 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apk add --no-cache \
    make \
    gettext \
    git \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    && pip install poetry==$POETRY_VERSION

WORKDIR /usr/local/src/hexlet-friends

COPY pyproject.toml poetry.lock ./

RUN poetry install $(if [[ "$DJANGO_ENV" != "development" ]]; then \
        echo "--no-dev"; \
        rm -rf ~/.cache/pypoetry; \
    fi)

COPY . ./

RUN adduser -D user \
    && chown -R user:user .

USER user

CMD ["make", "start"]
