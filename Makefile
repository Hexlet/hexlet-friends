.env:
	test ! -f .env && cp .env.example .env

build-production:
	pip install -r requirements.txt
	$(MAKE) collectstatic
	$(MAKE) migrate

build:
	uv run python manage.py migrate

check: lint test requirements.txt

collectstatic:
	uv run python manage.py collectstatic --no-input

compose-build: .env
	docker compose build

compose-clear:
	docker compose down -v || true

compose-down:
	docker compose down || true

compose-setup: compose-build
	docker compose run --rm django make setup

compose-start:
	docker compose up --abort-on-container-exit

compose-stop:
	docker compose stop || true

compose-sync:
	docker compose run --rm django make sync ARGS="$(ARGS)"

deploy:
	git push heroku

setup-pre-commit-hooks:
	uv run pre-commit install

install-dependencies: .env
	uv sync

install: install-dependencies setup-pre-commit-hooks

lint:
	uv run ruff check

migrate:
	uv run python manage.py migrate

requirements.txt:
	uv pip compile pyproject.toml -o requirements.txt

secretkey:
	uv run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

setup: install
	$(MAKE) migrate
	$(MAKE) updatesuperuser

updatesuperuser:
	uv run python manage.py updatesuperuser --username admin --email admin@mail.com

shell:
	uv run python manage.py shell_plus --plain

start-deploy:
	uv run gunicorn config.wsgi

start-production:
	uv run gunicorn -b 0.0.0.0:8000 config.wsgi:application

start:
	uv run python manage.py runserver 0.0.0.0:8000

sync:
	uv run python manage.py fetchdata $(ARGS)

test-coverage-report-xml:
	uv run coverage xml

test-coverage-report: test
	uv run coverage report -m $(ARGS)
	uv run coverage erase

test:
	uv run coverage run --source='.' manage.py test

transcompile:
	uv run django-admin compilemessages

load-dump:
	psql -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME) -p $(DB_PORT) -f dump.sql
# Need to have GNU gettext installed
transprepare:
	uv run django-admin makemessages --locale ru --add-location file
	uv run django-admin makemessages --locale ru --add-location file --domain djangojs

# Need to have graphviz installed
erd-dot:
	uv run python manage.py graph_models -a -g > erd.dot

erd-in-png: erd-dot
	dot -Tpng erd.dot -o erd.png

erd-in-pdf: erd-dot
	dot -Tpdf erd.dot -o erd.pdf

load-db:
	uv run python manage.py dbshell < dump_data/dump-hexlet-friends.sql

compose-load-db:
	docker-compose run --rm db make load-db

compose-setup: compose-load-db

.PHONY: install setup shell lint test check start sync secretkey requirements.txt
