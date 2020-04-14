release: python manage.py migrate
web: gunicorn config.wsgi --log-file -
clock: python -m contributors.utils.data_update_planner
