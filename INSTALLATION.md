# Установка и запуск приложения

---


Запустить приложение можно как с помощью Poetry, так и с помощью Docker.  

***Poetry* устанавливается командами:**

Linux \ OSX:  
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`  

Подробности установки и использования пакета **Poetry** доступны в [официальной документации](https://python-poetry.org/docs/).  
  
**Для установки **Docker** воспользуйтесь информацией с официального сайта [docs.docker.com](https://docs.docker.com/engine/install/)**

---

## 1. Установка

### 1.1 Клонирование репозитория и установка зависимостей:  

```commandline
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
```

**Установка зависимостей, если вы используете *Poetry***
```commandline
make install
```
Активировать виртуальное окружение
```commandline
poetry shell
```

**Установка зависимостей, если вы используете *Docker***
```commandline
make docker-install
```

---

### 1.2 Для работы с проектом потребуется задать значения переменным окружения в файле .env  
`GITHUB_AUTH_TOKEN` — Personal access token из [настроек GitHub](https://github.com/settings/tokens). Используется для запросов данных у GitHub.

Как его получить, если у вас его ещё нет:
> Переходите по ссылке выше, нажимаете кнопку ***Generate new token***. Github попросит ввести пароль от Github аккаунта.  
> В поле ***Note*** вводим любое понятное для вас название токена.  
> В области ***Select scopes*** ставим галочки напротив **delete:packages**, **delete_repo**, **public_repo**, **read:packages**. Остальное на ваш выбор.  
> Генерируем токен соответствующей кнопкой ***Generate token***

Значения для `GITHUB_WEBHOOK_TOKEN` и `SECRET_KEY` можно сгенерировать командой `make secretkey` в терминале в директории проекта или придумать.

Переменные `GITHUB_AUTH_CLIENT_ID` и `GITHUB_AUTH_CLIENT_SECRET` нужны для авторизации через GitHub.  
Получить значения для них можно, создав [OAuth application](https://github.com/settings/applications/new):  
> В поле ***Application name*** указываем ***hexlet-friends***  
> В поле ***Homepage URL*** указываем ***https://friends.hexlet.io/***  
> В поле ***Authorization callback URL*** указываем ***http://localhost:8000/auth/github/login***  
> 
> Остальное оставляем по умолчанию.  

После нажатия кнопки ***Register application*** в новом окне вы найдете ***Client ID*** для `GITHUB_AUTH_CLIENT_ID` и потребуется сгенерировать кнопкой ***Generate a new client secret*** токен для `GITHUB_AUTH_CLIENT_SECRET`  
Обратите внимание, что после того как вы покинете страницу, заново посмотреть токен будет нельзя, только генерировать заново и заносить в .env файл.

При работе с Poetry можно использовать SQLite, добавив `DB_ENGINE=SQLite` в .env файл. По умолчанию это значение отсутствует.  
Для работы с Docker, потребуется установленная PostgreSQL. Задать значения соответствующим переменным ***POSTGRES***.

--- 

### 1.3 Завершение установки  

#### *Poetry*
```commandline
make setup
```
#### *Docker*
```commandline
docker-compose run --rm django make setup
```
---
## 2. Наполнение базы данных  

Получить данные можно через интерфейс панели администрирования либо выполнив описанные команды.  

### *Poetry*  
**По именам организаций:**
```commandline
make sync ARGS='ORG [ORG ...]'
```
Example:
```commandline
make sync ARGS='Hexlet'
```
>Учитывайте, что в таком случае в базу данных будут добавляться все репозитории организации Hexlet. Это займёт продолжительно время. 

**По полным именам репозиториев:**
```commandline
make sync ARGS='--repo REPO [REPO ...]'
```
Example:
```commandline
make sync ARGS='--repo Hexlet/hexlet-friends'
```

#### При последующих обновлениях данных:
```commandline
make sync  
```  

---

## 3. Запуск сервера для разработки
### Poetry

```
make start
```

**После запуска сервера, перейти на адрес http://127.0.0.1:8000**

### Docker

```
make docker-start
```
**После запуска сервера, перейти на адрес http://127.0.0.1:8000**
