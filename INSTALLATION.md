# Installing and running the app

You can run the application using both uv and Docker.

**uv** is setup by the commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Details on installing and using the **uv** package are available in [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

To install **Docker**, use the information from the official website [docs.docker.com](https://docs.docker.com/engine/install/)

---

## 1. Installation

### 1.1 Cloning the repository and installing dependencies

```bash
git clone https://github.com/Hexlet/hexlet-friends
cd hexlet-friends
```

Installing dependencies if you use **uv**

```bash
make setup
```

Installing dependencies if you use **Docker**

```bash
make compose-build
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

You should also set `DEBUG=True` in .env file because by default content is loaded under the https protocol instead of http, witch is not supported by development server. Using debug also provides you with debug toolbar.

Admin login details:
- login: admin
- password: admin

---

### 1.3 Finishing the installation for *Docker*


```bash
make compose-setup
```

---

## 2. Filling the database

You can get the data through the interface of the administration panel or by running the described commands.

### **By organization name:**

*With uv*

```bash
make sync ARGS='ORG [ORG ...]'
```

Example:

```bash
make sync ARGS='hexlet-boilerplates'
```

*With Docker*

```bash
make compose-sync ARGS='ORG [ORG ...]'
```

Example:

```bash
make compose-sync ARGS='hexlet-boilerplates'
```

- Keep in mind that this will add all repositories of the organization to the database. This will take a long time.  
- Keep in mind that the github api has a limit of 5000 requests per hour. If you request data for an organization with a large number of repositories (e.g. Hexlet),  
you will get a 403 error at some point, and the data download will stop. In general, it is not necessary to upload all data for development. If the work on the task  
is related to a specific repository, you can upload data for a specific repository as described below.

**By full repository names:**

*uv*

```bash
make sync ARGS='--repo REPO [REPO ...]'
```

Example:

```bash
make sync ARGS='--repo Hexlet/hexlet-friends'
```

*Docker*

```bash
make compose-sync ARGS='--repo REPO [REPO ...]'
```

Example:

```bash
make compose-sync ARGS='--repo Hexlet/hexlet-friends'
```

#### On subsequent data updates

```bash
make sync
```

---

## 3. Running a server for development

### uv

```bash
make start
```

### Docker

```bash
make compose-start
```

## 4. Useful commands

### 4.1 Generate erd-diagrams
You can generate actual erd-diagrams based on project models in pdf or png format using the following commands:  

```
make erd-in-png
```  

```
make erd-in-pdf
```
