install:
	@poetry install
	@poetry run python manage.py migrate
	@echo Create a super user
	@poetry run python manage.py createsuperuser
	@cp .env.example .env

lint:
	@poetry run flake8

test:
	@poetry run python manage.py test

check: lint test

start: test
	@poetry run python manage.py runserver --noreload

sync:
	@poetry run python manage.py fetch_github
