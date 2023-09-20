install: .env
	poetry install --extras psycopg2-binary

compose-build: .env
	docker compose build

compose-setup: compose-build
	docker compose run --rm django make setup

.env:
	test ! -f .env && cp .env.example .env

migrate:
	poetry run python manage.py migrate

build:
	poetry install --extras psycopg2-binary
	poetry run python manage.py migrate

start-deploy:
	gunicorn config.wsgi

build-production:
	poetry install --extras psycopg2-binary
	$(MAKE) collectstatic

start-production:
	gunicorn -b 0.0.0.0:8000 config.wsgi:application

setup: migrate
	echo Create a super user
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell_plus --plain

# Need to have GNU gettext installed
transprepare:
	poetry run django-admin makemessages --locale ru --add-location file
	poetry run django-admin makemessages --locale ru --add-location file --domain djangojs

transcompile:
	poetry run django-admin compilemessages

collectstatic:
	poetry run python manage.py collectstatic --no-input

lint:
	poetry run flake8

test:
	poetry run coverage run --source='.' manage.py test

test-coverage-report: test
	poetry run coverage report -m $(ARGS)
	poetry run coverage erase

test-coverage-report-xml:
	poetry run coverage xml

check: lint test requirements.txt

start:
	poetry run python manage.py runserver 0.0.0.0:8000

compose-start:
	docker compose up --abort-on-container-exit

compose-stop:
	docker compose stop || true

compose-down:
	docker compose down || true

compose-clear:
	docker compose down -v || true

compose-sync:
	docker compose run --rm django make sync ARGS="$(ARGS)"

sync:
	poetry run python manage.py fetchdata $(ARGS)

secretkey:
	poetry run python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'

requirements.txt: poetry.lock
	poetry export --format requirements.txt --output requirements.txt --extras psycopg2 --without-hashes

deploy:
	git push heroku

.PHONY: install setup shell lint test check start sync secretkey
