import hmac

from django.conf import settings

from app.models import Contribution, Contributor, Organization, Repository


def signatures_match(payload_body, gh_signature):
    """Compares equality of signatures.

    The first is computed for the payload using the webhook token,
    the second comes from the request's header.
    """
    signature = 'sha1={0}'.format(
        hmac.new(
            settings.GITHUB_WEBHOOK_TOKEN.encode(),
            payload_body,
            'sha1',
        ).hexdigest(),
    )
    return hmac.compare_digest(signature, gh_signature)


class GitHubEvent(object):
    """Event representation."""

    event_types = {
        'commit': 'commits',  # TODO
        'pull_request': 'pull_requests',
        'issues': 'issues',
        'commit_comment': 'comments',
        'issue_comment': 'comments',
        'pull_request_review': 'comments',
        'pull_request_review_comment': 'comments',
    }

    def __init__(self, type_, action, sender, repository):
        """Initialization of an instance."""
        self.type = self.event_types[type_]
        self.action = action
        self.sender = sender
        self.repository = repository

    def update_database(self):
        """Updates the database with the event's data."""
        if self.action not in {'created', 'opened', 'submitted'}:
            return

        organization, _ = Organization.objects.get_or_create(
            id=self.repository['owner']['id'],
            defaults={
                'name': self.repository['owner']['login'],
                'html_url': self.repository['owner']['html_url'],
            },
        )

        repository, _ = Repository.objects.get_or_create(
            id=self.repository['id'],
            defaults={
                'name': self.repository['name'],
                'full_name': self.repository['full_name'],
                'html_url': self.repository['html_url'],
                'organization': organization,
            },
        )

        contributor, _ = Contributor.objects.get_or_create(
            id=self.sender['id'],
            defaults={
                'login': self.sender['login'],
                'name': self.sender.get('name'),    # TODO
                'avatar_url': self.sender['avatar_url'],
                'html_url': self.sender['html_url'],
            },
        )

        contribution, _ = Contribution.objects.update_or_create(
            repository=repository,
            contributor=contributor,
        )
        current_field_value = getattr(contribution, self.type)
        setattr(contribution, self.type, current_field_value + 1)
        contribution.save()
