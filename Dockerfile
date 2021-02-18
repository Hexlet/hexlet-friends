FROM python:3.8-alpine as builder

ENV VIRTUAL_ENV=/opt/venv \
    PATH=/root/.poetry/bin:$PATH

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev

RUN wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -O - | python > /dev/null

RUN python -m venv $VIRTUAL_ENV

WORKDIR /project/

COPY pyproject.toml poetry.lock ./

RUN poetry install --extras psycopg2-binary

FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=false \
    VIRTUAL_ENV=/opt/venv \
    PATH=/home/user/.poetry/bin:$PATH

RUN apk add --no-cache \
    gettext \
    git \
    make \
    postgresql-dev

WORKDIR /usr/local/src/hexlet-friends

RUN adduser -D user \
    && chown -R user:user ./

USER user

COPY --from=builder --chown=user:user /root/.poetry/ /home/user/.poetry/

COPY --from=builder --chown=user:user $VIRTUAL_ENV $VIRTUAL_ENV

COPY --chown=user:user ./ ./

CMD ["make", "start"]
