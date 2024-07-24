import hmac

from django.conf import settings
from django.utils import dateparse, timezone

from contributors.models import (
    CommitStats,
    Contribution,
    ContributionLabel,
    Contributor,
    IssueInfo,
    Organization,
    Repository,
)
from contributors.utils import github_lib as github


def signatures_match(payload_body, gh_signature):
    """Compare equality of signatures.

    The first is computed for the payload using the webhook token,
    the second comes from the request's header.
    """
    signature_body = hmac.new(
        settings.GITHUB_WEBHOOK_TOKEN.encode(),
        payload_body,
        'sha1',
    ).hexdigest()

    signature = f'sha1={signature_body}'
    return hmac.compare_digest(signature, gh_signature)


def update_database(event_type, payload):   # noqa: C901
    """Update the database with an event's data."""
    action = payload.get('action', 'created')
    if action not in {'created', 'opened', 'edited', 'closed', 'reopened'}:
        return
    sender = payload['sender']
    if sender['type'] == 'Bot':
        return
    repo = payload['repository']
    org = repo['owner']

    organization, _ = Organization.objects.get_or_create(
        id=org['id'],
        defaults={
            'name': org['login'],
            'html_url': org['html_url'],
        },
    )

    repository, _ = Repository.objects.get_or_create(
        id=repo['id'],
        defaults={
            'name': repo['name'],
            'full_name': repo['full_name'],
            'html_url': repo['html_url'],
            'organization': organization,
        },
    )

    contributor, _ = Contributor.objects.get_or_create(
        id=sender['id'],
        defaults={
            'login': sender['login'],
            'name': github.get_user_name(sender['url']),
            'avatar_url': sender['avatar_url'],
            'html_url': sender['html_url'],
        },
    )

    event_type_to_data_field_mapping = {
        'push': 'commits',
        'pull_request': 'pull_request',
        'issues': 'issue',
        'commit_comment': 'comment',
        'issue_comment': 'comment',
        'pull_request_review_comment': 'comment',
    }

    event_type_to_db_type_mapping = {
        'push': 'cit',
        'pull_request': 'pr',
        'issues': 'iss',
        'commit_comment': 'cnt',
        'issue_comment': 'cnt',
        'pull_request_review_comment': 'cnt',
    }

    contrib_data = payload[event_type_to_data_field_mapping[event_type]]
    contrib_type = event_type_to_db_type_mapping[event_type]

    # Special case for commits
    # push event
    commit_created_at = timezone.localtime(
        dateparse.parse_datetime(
            payload['commits'][0]['timestamp'],
        ),
        timezone.utc,
    ).strftime('%Y-%m-%dT%H:%M:%SZ')
    if event_type == 'push':
        for gh_commit in github.get_repo_commits_except_merges(
            organization, repository, {'since': commit_created_at},
        ):
            commit = Contribution.objects.create(
                repository=repository,
                contributor=contributor,
                id=gh_commit['sha'],
                type=contrib_type,
                html_url=gh_commit['html_url'],
                created_at=dateparse.parse_datetime(
                    gh_commit['commit']['author']['date'],
                ),
            )
            commit_extra_data = github.get_commit_data(
                organization, repository, commit.id,
            )
            commit_stats = commit_extra_data['stats']
            CommitStats.objects.create(
                commit=commit,
                additions=commit_stats['additions'],
                deletions=commit_stats['deletions'],
            )
    # Actions for other types of events:
    # commit_comment, issue_comment, pull_request_review_comment
    # issues, pull_request
    else:
        contrib, _ = Contribution.objects.get_or_create(
            id=contrib_data['id'],
            defaults={
                'repository': repository,
                'contributor': contributor,
                'type': contrib_type,
                'html_url': contrib_data['html_url'],
                'created_at': dateparse.parse_datetime(
                    contrib_data['created_at'],
                ),
            },
        )

        for label in contrib_data['labels']:
            label_name, _ = ContributionLabel.objects.get_or_create(
                name=label["name"],
            )
            contrib.labels.add(label_name)

        if contrib.type == 'iss':
            IssueInfo.objects.update_or_create(
                issue=contrib,
                defaults={
                    'title': contrib_data['title'],
                    'is_open': contrib_data['state'] == 'open',
                },
            )
