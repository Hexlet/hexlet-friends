# Installing and running the app

You can run the application using both Poetry and Docker.

**Poetry** is setup by the commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Details on installing and using the **Poetry** package are available in [official documentation](https://python-poetry.org/docs/).

To install **Poetry** you need **Python 3.7+** use the information from the official website [python.org](https://www.python.org/downloads/)

To install **Docker**, use the information from the official website [docs.docker.com](https://docs.docker.com/engine/install/)

---

## 1. Installation

### 1.1 Cloning the repository and installing dependencies

```bash
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
```

Installing dependencies if you use **Poetry**

```bash
make install
```

Activate virtual environment

```bash
source $HOME/.cache/pypoetry/virtualenvs/<name of the created environment>/bin/activate
```

Installing dependencies if you use **Docker**

```bash
make docker-install
```

---

### 1.2 To work with the project, you will need to set the values of the environment variables in the .env file

`GITHUB_AUTH_TOKEN` — Personal access token from [GitHub's settings](https://github.com/settings/tokens). Used to query data on GitHub.

How do you get it if you don't have it yet:

- Go to the link above, click the ***Generate new token*** button. Github will ask you to enter the password for your Github account.
- In the ***Note*** field, enter any token name you understand.
- In the ***Select scopes*** area, check the ***repo*** ***Full control of private repositories*** and ***delete_repo*** ***Delete repositories***, the rest is your choice.
- Generate a token with the appropriate button ***Generate token***

The values for `GITHUB_WEBHOOK_TOKEN` and `SECRET_KEY` can be generated with the terminal command `make secretkey` in the project directory or you can make one up.

The `GITHUB_AUTH_CLIENT_ID` and `GITHUB_AUTH_CLIENT_SECRET` variables are needed for authorization through GitHub.

You can get the values for them by creating [OAuth application](https://github.com/settings/applications/new):
- In the ***Application name*** field specify ***hexlet-friends***
- In the ***Homepage URL*** field specify ***<https://friends.hexlet.io/>***
- In the ***Authorization callback URL*** field specify ***<http://localhost:8000/auth/github/login>***
- Leave the rest as default.

After clicking ***Register application*** in the new window you will find ***Client ID*** for `GITHUB_AUTH_CLIENT_ID` and will need to generate with ***Generate a new client secret*** token for `GITHUB_AUTH_CLIENT_SECRET`.
Note that after you leave the page, you can't look at the token again, you just have to generate it again and put it into an .env file.

You can use SQLite with Poetry by adding `DB_ENGINE=SQLite` to the .env file. By default, this value is not present.
If PostgreSQL is installed, set values to the corresponding variables ***POSTGRES***.

---

### 1.3 Finishing the installation

#### *Poetry*

```bash
make setup
```

#### *Docker*


```bash
docker-compose run --rm django make setup
```

---

## 2. Filling the database

You can get the data through the interface of the administration panel or by running the described commands.

### *Poetry*

**By organization name:**

```bash
make sync ARGS='ORG [ORG ...]'
```

Example:

```bash
make sync ARGS='Hexlet'
```

>Keep in mind that this will add all repositories of the Hexlet organization to the database. This will take a long time.

**By full repository names:**

```bash
make sync ARGS='--repo REPO [REPO ...]'
```

Example:

```bash
make sync ARGS='--repo Hexlet/hexlet-friends'
```

#### On subsequent data updates

```bash
make sync
```

---

## 3. Running a server for development

### Poetry

```bash
make start
```

### Docker

```bash
make docker-start
```
