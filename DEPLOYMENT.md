# Развертывание Hexlet-Friends на Render

Для деплоя понадобится аккаунт на Render. Достаточно бесплатного тарифного плана, но в нём нет консоли в браузере, поэтому будет рассмотрено заполнение БД через локальное приложение.

## Подготовка базы данных PostgreSQL

*Убедитесь, что вы используете одинаковый `SECRET_KEY` при работе с одной БД из разных приложений.*

### Создание

1. Из Dashboard нажмите *+ New* -> *PostgreSQL*;
2. Задайте имя и ближайший регион. Остальные поля можно оставить по умолчанию;
3. Нажмите *Create Database* и дождитесь окончания процесса;
4. В информации о БД, в разделе *Info* находятся **Internal Database URL** и **External Database URL**. Используйте их далее.

### Заполнение

1. В локальном приложении укажите следующие переменные окружения в *[.env](.env.example)*:

    ```text
    DATABASE_URL=<External Database URL>
    SECRET_KEY=<Секретный ключ для БД>
    GITHUB_AUTH_TOKEN=<Ваш Github токен>
    DB_ENGINE=<Должна быть пустой или отсутствовать>
    ```

    *Для получения `GITHUB_AUTH_TOKEN` см. [INSTALLATION.md](INSTALLATION.md#12-to-work-with-the-project-you-will-need-to-set-the-values-of-the-environment-variables-in-the-env-file);*
2. Выполните команды:

    ```bash
    make migrate
    make sync ARGS='--repo Hexlet/hexlet-friends'
    ```

    Параметр `ARGS` может быть любым, согласно [INSTALLATION.md](INSTALLATION.md#2-filling-the-database);
3. Дождитесь окончания процесса. Желательно после этого удалить значение `DATABASE_URL`, во избежание путаницы.

## Создание веб-приложения

Теперь когда БД готова, можно деплоить само приложение.

1. Из Dashboard нажмите *+ New* -> *Web Service*;
2. Выберите желаемый репозиторий. Если его нет в списке - убедитесь что вы подключили Github аккаунт (*Connect account*) и предоставили доступ к репозиторию (*Configure account*);
3. Заполните следующие параметры:

   * Name: <Желаемое имя>
   * Region: <Ближайший регион>
   * Branch: <Ваша ветка с фичей>
   * Root Directory: <Оставить по умолчанию>
   * Runtime: Python 3
   * Build Command:

    ```bash
    make build-production
    ```

   * Start Command:

    ```bash
    make start-production
    ```

4. Нажмите *Environment* и введите следующие переменные окружения:

    ```text
    DATABASE_URL=<Internal Database URL>
    DEBUG=FALSE
    GITHUB_AUTH_CLIENT_ID=<Нужна для авторизации через GitHub>
    GITHUB_AUTH_CLIENT_SECRET=<Нужна для авторизации через GitHub>
    PYTHON_VERSION=<Желаемая версия Python>
    GITHUB_AUTH_TOKEN=<Токен личного доступа из настроек GitHub>
    GITHUB_WEBHOOK_TOKEN=<можно сгенерировать командой терминала make secretkey в каталоге проекта или создать самостоятельно>
    SECRET_KEY=<можно сгенерировать командой терминала make secretkey в каталоге проекта или создать самостоятельно>
	```
	Для получения `GITHUB_AUTH_CLIENT_ID`, `GITHUB_AUTH_CLIENT_SECRET`, `GITHUB_AUTH_TOKEN` см. [INSTALLATION.md](INSTALLATION.md#12-to-work-with-the-project-you-will-need-to-set-the-values-of-the-environment-variables-in-the-env-file)

5. Нажмите *Create Web Service* и дождитесь окончания процесса. В информации о приложении вы найдёте адрес и логи. Всё готово.

## Дополнительно: применение фикстуры

Процесс скачивания исходных данных с репозиториев может занимать длительное время.
Поэтому стоит сохранить эти данные в фикстуру, чтобы в будущем сразу применить их к БД.
Это возможно как для локального SQLite, так и для удалённого PostgreSQL.
Будет рассмотрено сохранение БД в JSON файл db_fixture.json (имя может быть любым) для последующего восстановления из него.
Предполагается, что локальное приложение настроено для работы с БД и указаны переменные окружения:

* `SECRET_KEY`
* Для SQLite добавочно `DB_ENGINE=SQLite`
* Для PostgreSQL добавочно `DATABASE_URL`

### Сохранение фикстуры

Выполните команду:

```bash
uv run python manage.py dumpdata --indent 2 > db_fixture.json
```

### Применение фикстуры

*Не забудьте применить миграции `make migrate` перед записью фикстуры в БД.*
Выполните команду:

```bash
uv run python manage.py loaddata db_fixture.json
```
