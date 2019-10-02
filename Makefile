# test/setup/start/install/

lint:
	flake8 --config=setup.cfg

test:
	python manage.py test
