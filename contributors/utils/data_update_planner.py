import datetime
import os

import django
from apscheduler.schedulers.background import BlockingScheduler
from django.core.management import call_command


def fetch_data():
    """Call the appropriate management command."""
    call_command('fetchdata')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
scheduler = BlockingScheduler()
scheduler.add_job(
    fetch_data,
    'interval',
    hours=os.getenv('UPDATE_INTERVAL_HOURS', 24),
    start_date=datetime.datetime.now() + datetime.timedelta(minutes=10),
)
scheduler.start()
