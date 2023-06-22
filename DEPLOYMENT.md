## Развертывание Hexlet-Friends на Railway

1. Создайте новый проект на Railway. Для успешного деплоя приложения вам понадобится база данных `PostgreSQL` и приложение
2. Для добавления БД при создании проекта выберите `Provision PostgreSQL`
3. После добавления БД, нажмите `+ New` -> `Github Repo`. В выпадающем списке выберите свой репозиторий с `Hexlet-friends`. Здесь возможно понадобится дать доступы Railway к вашим репозитория, если ранее вы их не настроили
4. Переходим в настройки нашего приложения. Нам необходимо:

   - настроить переменные окружения на вкладке `Variables`. Вам понадобятся:

        - `PORT` - присвойте значение 8000, после нажмите на три вертикальные точки справа от переменной и выберите `Promote` - это позволит использовать данный порт для входа в приложение.
        - `GITHUB_AUTH_TOKEN`
        - `SECRET_KEY`
        - `POSTGRES_DB`
        - `POSTGRES_USER`
        - `POSTGRES_PASSWORD`
        - `POSTGRES_HOST`
        - `POSTGRES_PORT`

    Переменные `PostgreSQL` можно использовать через `Add reference` при создании переменной для приложения

   - выбрать ветку, изменения из которой будут отслеживаться в меню `Automatic Deployments` на вкладке `Settings`
   - в графе `Domains` нажмем кнопку `Generate Domain` для генерации домена для доступа к приложению
   - в меню `Deployments` открывает `Deploy Logs` и убеждаемся, что все работает

    ```bash
    Performing system checks...
    ﻿System check identified no issues (0 silenced).
    ﻿You have 36 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, contributors, custom_auth, sessions.
    ﻿Run 'python manage.py migrate' to apply them.
    ﻿June 21, 2023 - 09:22:50
    ﻿Django version 4.1.9, using settings 'config.settings'
    ﻿Starting development server at http://0.0.0.0:8000/
    ﻿Quit the server with CONTROL-C.
    ```

5. Как видим миграции не приняты, для этого перейдем вновь на вкладку `Settings` в настройках приложения:

   - в меню `Start Command` укажем `python manage.py migrate`
   - произойдет редеплой в ходе которого применятся миграции. Отследить выполнение команды можно в логах приложения
   - удалим команду из `Start Command`
   - убедимся по логам, что все в порядке

    ```bash
    Performing system checks...
    ﻿Django version 4.1.9, using settings 'config.settings'
    ﻿Starting development server at http://0.0.0.0:8000/
    ﻿Quit the server with CONTROL-C.
    ```

6. Если необходимо выполнить заполнение БД, то в `Start Command` следует указать команду `python manage.py fetchdata <organization name>`
7. Перейдем по ссылке в `Domains` в `Settings` и убедимся, что приложение работает
