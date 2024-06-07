import json

from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from contributors.utils.github_webhook import (
    signatures_match,
    update_database,
)


@method_decorator(csrf_exempt, name='dispatch')
class EventHandler(View):
    """Handles GitHub events."""

    def post(self, request):
        """Get data from request and update the database."""
        payload = request.body
        signature = request.headers.get('X-Hub-Signature')
        if not signature or not signatures_match(payload, signature):
            return HttpResponseForbidden("Forbidden action.")

        event_type = request.headers.get('X-GitHub-Event')
        payload = json.loads(request.POST.get('payload'))
        update_database(event_type, payload)

        return HttpResponse("Success.")
