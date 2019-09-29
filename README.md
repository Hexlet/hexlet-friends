# hexlet-friends


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

# Цель

*hexlet-friends* - сервис, который будет отслеживает все репозитории хекслета.
Строит leaderboard по людям, которые учавствуют в этих проектах.
Сервис работает автоматизированно.

