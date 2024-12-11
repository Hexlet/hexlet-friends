release: python manage.py migrate
web: gunicorn config.wsgi --log-file -
worker: celery -A config worker -l info --concurrency=4
beat: celery -A config beat -l info
