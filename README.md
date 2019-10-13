[![Build Status](https://travis-ci.com/Hexlet/hexlet-friends.svg?branch=master)](https://travis-ci.com/Hexlet/hexlet-friends)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

# hexlet-friends

Сервис отслеживающий и анализирующий open-source проекты хекслета на github по
таким параметрам как количество коммитов, pull-реквестов, issues. В результате
строится leaderboard участников с различными ачивками для мотивации. Сервис
работает автоматизированно.

# Как развернуть проект

```shell script
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
poetry install
python manage.py migrate
```

```shell script
python manage.py runserver
```

Проект использует переменные окружения, пример в _.env.example_
