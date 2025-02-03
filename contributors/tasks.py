from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

from contributors.management.commands.fetchdata import ORGANIZATIONS

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def sync_github_data(self, owners=None, repos=None):
    try:
        orgs = [org.name for org in ORGANIZATIONS]
        logger.info(orgs)
        call_command("fetchdata", orgs or ["hexlet"], repo=repos or [])

    except Exception as exc:
        logger.error(f"Failed to sync GitHub data: {exc}")
        self.retry(exc=exc, countdown=60 * (2**self.request.retries))
