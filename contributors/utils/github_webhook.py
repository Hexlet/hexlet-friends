import hmac

from django.conf import settings

from contributors.models import (
    Contribution,
    Contributor,
    Organization,
    Repository,
)
from contributors.utils.fetch_info_from_github import (
    get_commit_stats_for_contributor,
    get_name_of_contributor,
)


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


def update_database(type_, action, sender, repository):
    """Updates the database with an event's data."""
    if action not in {'created', 'opened', 'submitted'}:
        return

    type_to_field_mapping = {
        'push': 'commits',
        'pull_request': 'pull_requests',
        'issues': 'issues',
        'commit_comment': 'comments',
        'issue_comment': 'comments',
        'pull_request_review': 'comments',
        'pull_request_review_comment': 'comments',
    }

    organization, _ = Organization.objects.get_or_create(
        id=repository['owner']['id'],
        defaults={
            'name': repository['owner']['login'],
            'html_url': repository['owner']['html_url'],
        },
    )

    repository, _ = Repository.objects.get_or_create(
        id=repository['id'],
        defaults={
            'name': repository['name'],
            'full_name': repository['full_name'],
            'html_url': repository['html_url'],
            'organization': organization,
        },
    )

    contributor, _ = Contributor.objects.get_or_create(
        id=sender['id'],
        defaults={
            'login': sender['login'],
            'name': get_name_of_contributor(sender['url']),
            'avatar_url': sender['avatar_url'],
            'html_url': sender['html_url'],
        },
    )

    contribution, _ = Contribution.objects.update_or_create(
        repository=repository,
        contributor=contributor,
    )

    # Special case for commits
    if type_ == 'push':
        commits_total, additions, deletions = get_commit_stats_for_contributor(
            repository.full_name,
            contributor.id,
        )
        contribution.commits = commits_total
        contribution.additions = additions
        contribution.deletions = deletions
    # Actions for other types of events
    else:
        field = type_to_field_mapping[type_]
        current_field_value = getattr(contribution, field)
        setattr(contribution, field, current_field_value + 1)

    contribution.save()
