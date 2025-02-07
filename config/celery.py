import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
# This will look for a 'tasks.py' file in each app directory
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """A simple task for testing Celery setup"""
    print(f"Request: {self.request!r}")
