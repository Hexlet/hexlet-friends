[![](https://github.com/Hexlet/hexlet-friends/workflows/CI/badge.svg)](https://github.com/Hexlet/hexlet-friends/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/maintainability)](https://codeclimate.com/github/Hexlet/hexlet-friends/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/test_coverage)](https://codeclimate.com/github/Hexlet/hexlet-friends/test_coverage)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# Hexlet Friends
Сервис для отслеживания вклада участников сообщества Хекслет в его open-source проекты на GitHub.

Вклад &mdash; issues, pull requests, commits, comments.

## Установка и настройка

### 0. Убедиться, что в системе установлены **poetry** и **make**.

### 1. Выполнить команды:

```
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
make install
```

### 2. Задать значения переменным окружения в _.env_:

`GITHUB_AUTH_TOKEN` &mdash; Personal access token из [настроек GitHub](https://github.com/settings/tokens).

Значения для `GITHUB_WEBHOOK_TOKEN` и `SECRET_KEY` можно сгенерировать командой `make secretkey`.

`DEBUG=True`

### 3. Выполнить команду `make setup`.

## Наполнение базы данных

По именам организаций:

```
make sync ARGS='ORG [ORG ...]'
```

По __полным__ именам репозиториев (org_name/repo_name):

```
make sync ARGS='--repo REPO [REPO ...]'
```

Последующее обновление данных:
```
make sync
```

## Запуск сервера для разработки

```
make start
```

## Локализация текста

Требуется утилита **gettext**.

1. `make transprepare` &mdash; подготовить файл **locale/ru/LC_MESSAGES/django.po**.
2. Внести изменения в этот файл.
3. Выполнить `make transcompile`.
