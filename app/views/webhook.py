import json

from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.utils.github_webhook import GitHubEvent, signatures_match


@method_decorator(csrf_exempt, name='dispatch')
class EventHandler(View):
    """Handles GitHub events."""

    def post(self, request):
        """Gets data from request and updates the database."""
        payload = request.body
        signature = request.headers.get('X-Hub-Signature')
        if not signature or not signatures_match(payload, signature):
            return HttpResponseForbidden("Forbidden action.")

        event_type = request.headers.get('X-GitHub-Event')
        payload = json.loads(request.POST.get('payload'))
        event = GitHubEvent(
            event_type,
            payload.get('action'),
            payload['sender'],
            payload['repository'],
        )
        event.update_database()

        return HttpResponse("Success.")
