.env:
	test ! -f .env && cp .env.example .env

build-production:
	poetry install --extras psycopg2-binary
	$(MAKE) collectstatic
	$(MAKE) migrate

build:
	poetry install --extras psycopg2-binary
	poetry run python manage.py migrate

check: lint test requirements.txt

collectstatic:
	poetry run python manage.py collectstatic --no-input

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
	poetry run pre-commit install

install-dependencies: .env
	poetry install --extras psycopg2-binary

install: install-dependencies setup-pre-commit-hooks

lint:
	poetry run flake8

migrate:
	poetry run python manage.py migrate

requirements.txt: poetry.lock
	poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes

secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

setup: install
	$(MAKE) migrate
	poetry run python manage.py createsuperuser --noinput --username admin --email admin@mail.com

shell:
	poetry run python manage.py shell_plus --plain

start-deploy:
	gunicorn config.wsgi

start-production:
	gunicorn -b 0.0.0.0:8000 config.wsgi:application

start:
	poetry run python manage.py runserver 0.0.0.0:8000

sync:
	poetry run python manage.py fetchdata $(ARGS)

test-coverage-report-xml:
	poetry run coverage xml

test-coverage-report: test
	poetry run coverage report -m $(ARGS)
	poetry run coverage erase

test:
	poetry run coverage run --source='.' manage.py test

transcompile:
	poetry run django-admin compilemessages

# Need to have GNU gettext installed
transprepare:
	poetry run django-admin makemessages --locale ru --add-location file
	poetry run django-admin makemessages --locale ru --add-location file --domain djangojs

# Need to have graphviz installed
erd-dot:
	poetry run python manage.py graph_models -a -g > erd.dot

erd-in-png: erd-dot
	dot -Tpng erd.dot -o erd.png

erd-in-pdf: erd-dot
	dot -Tpdf erd.dot -o erd.pdf

.PHONY: install setup shell lint test check start sync secretkey
