[![](https://github.com/Hexlet/hexlet-friends/workflows/CI/badge.svg)](https://github.com/Hexlet/hexlet-friends/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/maintainability)](https://codeclimate.com/github/Hexlet/hexlet-friends/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/test_coverage)](https://codeclimate.com/github/Hexlet/hexlet-friends/test_coverage)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# Hexlet Friends
Сервис для отслеживания вклада участников сообщества Хекслет в его open-source проекты на GitHub.

Вклад &mdash; issues, pull requests, commits, comments.

## Установка

Установить make.
Для работы с Poetry (без Docker) установить Poetry.
Для работы с Docker установить Docker Engine и Docker Compose.

### 1. Склонировать репозиторий

```
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
```

### 2. Установить зависимости

### Poetry

```
make install
```

### Docker

```
make .env
docker-compose build
```

### 3. Задать значения переменным окружения в *.env*

`GITHUB_AUTH_TOKEN` &mdash; Personal access token из [настроек GitHub](https://github.com/settings/tokens). Используется для запросов данных у GitHub.

Значения для `GITHUB_WEBHOOK_TOKEN` и `SECRET_KEY` можно сгенерировать командой `make secretkey` или придумать.

Переменные `GITHUB_AUTH_CLIENT_ID` и `GITHUB_AUTH_CLIENT_SECRET` нужны для авторизации через GitHub;
получить значения для них можно [создав OAuth application](https://github.com/settings/applications/new).
В поле *Authorization callback URL* нужно указать http://localhost:8000/auth/github/login.

При работе с Poetry можно использовать SQLite, добавив `DB_ENGINE=SQLite`.
Если установлена PostgreSQL, задать значения соответствующим переменным `POSTGRES`.

### 4. Завершить настройку

### Poetry

```
make setup
```

### Docker

```
docker-compose run --rm django make setup
```

## Наполнение базы данных

Получить данные можно через интерфейс панели администрирования либо выполнив описанные команды. Для Docker перед этими командами надо добавить `docker-compose run --rm django`.

По именам организаций:

```
make sync ARGS='ORG [ORG ...]'
```

По **полным** именам репозиториев (*org_name/repo_name*):

```
make sync ARGS='--repo REPO [REPO ...]'
```

Последующее обновление данных:

```
make sync
```

## Запуск сервера для разработки

### Poetry

```
make start
```

### Docker

```
docker-compose up
```

## Локализация текста

Установить **gettext** (при работе с Poetry).

1. Выполнить `make transprepare` &mdash; подготовка файлов ***.po** в директории **locale/ru/LC_MESSAGES**.
2. Внести изменения в эти файлы.
3. Выполнить `make transcompile`.
