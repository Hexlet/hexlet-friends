from urllib.parse import parse_qs, urlparse

import requests
from django.conf import settings

from contributors.utils.misc import merge_dicts

GITHUB_API_URL = 'https://api.github.com'


class GitHubError(Exception):
    """GitHub error."""


class Accepted(GitHubError):
    """HTTP 202 Response."""


class NoContent(GitHubError):
    """HTTP 204 Response."""


class NoContributorsError(GitHubError):
    """A repository has no contributors."""


class ContributorNotFoundError(GitHubError):
    """A particular contributor was not found."""


def get_headers():
    """Return headers to use in a request."""
    return {'Authorization': f'token {settings.GITHUB_AUTH_TOKEN}'}


def get_one_item_at_a_time(url, additional_params=None, session=None):
    """Return data from all pages (one instance at a time)."""
    query_params = {'page': 1, 'per_page': 100}
    query_params.update(additional_params or {})
    req = session or requests
    response = req.get(url, headers=get_headers(), params=query_params)
    response.raise_for_status()
    yield from response.json()

    pages_count = get_pages_count(response.links)
    while query_params['page'] < pages_count:
        query_params['page'] += 1
        response = req.get(
            url, headers=get_headers(), params=query_params,
        )
        response.raise_for_status()
        yield from response.json()


def get_whole_response_as_json(url, session=None):
    """Return data as given by GitHub (a batch)."""
    req = session or requests
    response = req.get(url, headers=get_headers())
    response.raise_for_status()
    if response.status_code == requests.codes.no_content:
        raise NoContent("204 No Content")
    elif response.status_code == requests.codes.accepted:
        raise Accepted("202 Accepted. No cached data. Retry.")
    return response.json()


def get_org_data(org, session=None):
    """Return an organization's data."""
    url = f'{GITHUB_API_URL}/orgs/{org}'
    return get_whole_response_as_json(url, session)


def get_repo_data(repo, session=None):
    """Return a repository's data."""
    url = f'{GITHUB_API_URL}/repos/{repo}'
    return get_whole_response_as_json(url, session)


def get_user_data(user, session=None):
    """Return a user's data."""
    url = f'{GITHUB_API_URL}/users/{user}'
    return get_whole_response_as_json(url, session)


def get_user_name(url, session=None):
    """Return a user's name."""
    return get_whole_response_as_json(url, session)['name']


def get_org_repos(org, session=None):
    """Return repositories of an organization."""
    url = f'{GITHUB_API_URL}/orgs/{org}/repos'
    return get_one_item_at_a_time(url, {'type': 'sources'}, session)


def get_repo_contributors(owner, repo, session=None):
    """Return contributors for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/stats/contributors'
    contributors = []
    for contributor in get_whole_response_as_json(url, session):
        contributor['login'] = contributor['author']['login']
        contributors.append(contributor)
    return contributors


def get_commit_data(owner, repo, ref, session=None):
    """Return data for a commit."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{ref}'
    return get_whole_response_as_json(url, session)


def get_repo_commits(owner, repo, query_params=None, session=None):
    """Return all commits for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/commits'
    return get_one_item_at_a_time(url, query_params, session)


def get_repo_commits_except_merges(
    owner, repo, query_params=None, session=None,
):
    """Return all commits for a repository except for merge commits."""
    return (
        commit for commit in get_repo_commits(
            owner, repo, query_params, session,
        ) if len(commit['parents']) < 2
    )


def get_repo_prs(owner, repo, session=None):
    """Return all pull requests for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/pulls'
    query_params = {'state': 'all'}
    return get_one_item_at_a_time(url, query_params, session)


def get_repo_issues(owner, repo, session=None):
    """
    Return all issues for a repository.

    Every pull request is an issue, but not every issue is a pull request.
    Identify pull requests by the `pull_request` key.
    [issue for issue in issues if 'pull_request' not in issue]
    """
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/issues'
    query_params = {'state': 'all'}
    return get_one_item_at_a_time(url, query_params, session)


def get_repo_comments(owner, repo, session=None):
    """Return all comments for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/comments'
    return get_one_item_at_a_time(url, session=session)


def get_comments_for_issue(owner, repo, issue_number, session=None):
    """Return all comments for an issue."""
    url = (
        f'{GITHUB_API_URL}/repos/{owner}/{repo}/issues/{issue_number}/comments'
    )
    return get_one_item_at_a_time(url, session=session)


def get_repo_issue_comments(owner, repo, session=None):
    """Return all issue comments for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/issues/comments'
    return get_one_item_at_a_time(url, session=session)


def get_review_comments_for_pr(owner, repo, pr_number, session=None):
    """Return all review comments for a pull request."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments'
    return get_one_item_at_a_time(url, session=session)


def get_repo_review_comments(owner, repo, session=None):
    """Return all review comments for a repository."""
    url = f'{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/comments'
    return get_one_item_at_a_time(url, session=session)


def get_all_types_of_comments(owner, repo, session=None):
    """Return all types of comments for a repository."""
    commit_comments = [
        comment for comment in get_repo_comments(owner, repo, session)
    ]
    issue_comments = [
        comment for comment in get_repo_issue_comments(owner, repo, session)
    ]
    review_comments = [
        comment for comment in get_repo_review_comments(owner, repo, session)
    ]
    comments = []
    comments.extend(commit_comments)
    comments.extend(issue_comments)
    comments.extend(review_comments)
    yield from comments


def get_total_contributions_per_user(contributions, author_field_name):
    """Return total numbers of contributions of a specific type per user."""
    users_contributions_totals = {}
    for contribution in contributions:
        author = contribution.get(author_field_name)
        if not author:  # Deleted user
            continue
        login = author.get('login')
        users_contributions_totals[login] = (
            users_contributions_totals.get(login, 0) + 1
        )
    return users_contributions_totals


def get_total_changes_per_user(contributors, change_type):
    """Return total numbers of changes of `type` made by each user."""
    total_changes_per_user = {}
    for contribution in contributors:
        login = contribution['login']
        total_changes_per_user[login] = sum(
            week[change_type] for week in contribution['weeks']
        )
    return total_changes_per_user


def get_total_prs_per_user(prs):
    """Return total numbers of pull requests per user."""
    return get_total_contributions_per_user(prs, 'user')


def get_total_commits_per_user(commits):
    """Return total numbers of commits per user."""
    return get_total_contributions_per_user(commits, 'author')


def get_total_commits_per_user_excluding_merges(owner, repo, session):
    """Return total numbers of commits per user excluding merge commits."""
    contributors = get_repo_contributors(owner, repo, session)
    return {
        contributor['login']: contributor['total']
        for contributor in contributors
    }


def get_total_issues_per_user(issues):
    """Return total numbers of issues per user."""
    return get_total_contributions_per_user(issues, 'user')


def get_total_comments_per_user(comments):
    """Return total numbers of comments per user."""
    return get_total_contributions_per_user(comments, 'user')


def get_total_additions_per_user(contributors):
    """Return total numbers of additions per user."""
    return get_total_changes_per_user(contributors, 'a')


def get_total_deletions_per_user(contributors):
    """Return total numbers of deletions per user."""
    return get_total_changes_per_user(contributors, 'd')


def get_pages_count(link_headers):
    """Return a number of pages for a resource."""
    if 'last' in link_headers:
        return int(
            parse_qs(urlparse(link_headers['last']['url']).query)['page'][0],
        )
    return 1


def get_commit_stats_for_contributor(repo_full_name, contributor_id):
    """Return numbers of commits, additions, deletions of a contributor."""
    org_name, repo_name = repo_full_name.split('/')
    try:
        contributors = get_repo_contributors(org_name, repo_name)
    except NoContent:
        raise NoContributorsError(
            "Nobody has contributed to this repository yet",
        ) from None

    try:
        contributor_stats = [
            stats for stats in contributors
            if stats['author']['id'] == contributor_id
        ][0]
    except IndexError:
        raise ContributorNotFoundError(
            "No such contributor in this repository",
        ) from None

    totals = merge_dicts(*contributor_stats['weeks'])

    return totals['c'], totals['a'], totals['d']


def get_data_of_orgs_and_repos(*, org_names=None, repo_full_names=None):  # noqa: C901,R701,E501
    """Return data of organizations and their repositories from GitHub."""
    if not (org_names or repo_full_names):
        raise ValueError("Neither org_names nor repo_full_names is provided")
    data_of_orgs_and_repos = {}
    with requests.Session() as session:
        if org_names:
            for org_name in org_names:
                data_of_orgs_and_repos[org_name] = {
                    'details': get_org_data(org_name, session),
                    'repos': [
                        repo for repo in get_org_repos(
                            org_name, session,
                        )
                    ],
                }
        elif repo_full_names:
            # Construct a dictionary of names {org: [repo, repo, ...]}
            names_of_orgs_and_repos = {}
            for repo_full_name in repo_full_names:
                org_name, repo_name = repo_full_name.split('/')
                repos_of_org = names_of_orgs_and_repos.setdefault(org_name, [])
                repos_of_org.append(repo_name)

            for org_name, repo_names in names_of_orgs_and_repos.items():
                data_of_orgs_and_repos[org_name] = {
                    'details': get_org_data(org_name, session),
                    'repos': [
                        repo for repo in get_org_repos(
                            org_name, session,
                        )
                        if repo['name'] in repo_names
                    ],
                }
    return data_of_orgs_and_repos
