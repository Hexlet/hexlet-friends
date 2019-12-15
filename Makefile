install:
	@poetry install
	@poetry run python manage.py migrate
	@echo Create a super user
	@poetry run python manage.py createsuperuser

shell:
	@poetry run python manage.py shell

# Need to have GNU gettext installed
transprepare:
	@poetry run django-admin makemessages --add-location file

transcompile:
	@poetry run django-admin compilemessages

lint:
	@poetry run flake8

test:
	@poetry run python manage.py test

check: lint test requirements.txt

start: test
	@poetry run python manage.py runserver --noreload

sync:
	@poetry run python manage.py fetchdata

requirements.txt: poetry.lock
	@poetry export --format requirements.txt --output requirements.txt

.PHONY: install shell transprepare transcompile lint test check start sync
