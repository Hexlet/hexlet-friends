from collections import Counter
from urllib.parse import parse_qs, urlparse

import requests
from django.conf import settings

DEFAULT_USER = 'Hexlet'
PAGE_KEY = 'page'
GITHUB_API = 'https://api.github.com'


class GitHubError(Exception):
    """GitHub error."""


class NoContributorsError(GitHubError):
    """A repository has no contributors."""


class ContributorNotFoundError(GitHubError):
    """A particular contributor was not found."""


def fetch_all_repos_for_user(user=DEFAULT_USER):
    """Fetch user repository."""
    url = f'{GITHUB_API}/users/{user}/repos'
    return fetch_from_github(url)


def fetch_commits_for_repo(repo, user=DEFAULT_USER):
    """Fetch repository commits."""
    url = f'{GITHUB_API}/repos/{user}/{repo}/commits'
    return fetch_from_github(url)


def fetch_pr_for_repo(repo, user=DEFAULT_USER):
    """Fetch repository pr's."""
    url = f'{GITHUB_API}/repos/{user}/{repo}/pulls'
    request_params = {'state': 'closed'}
    return fetch_from_github(url, request_params)


def fetch_issues_for_repo(repo, user=DEFAULT_USER):
    """
    Fetch repository issues.

    GitHub's REST API v3 considers every pull request an issue,
    but not every issue is a pull request. For this reason,
    "Issues" endpoints may return both issues and pull requests in the response.
    You can identify pull requests by the pull_request key.

    Need filter(lambda x: x.get('pull_request', False), issues)
    """
    url = f'{GITHUB_API}/repos/{user}/{repo}/issues'
    request_params = {'state': 'all'}
    return fetch_from_github(url, request_params)


def fetch_comments_for_repo_issue(repo, number_issue, user=DEFAULT_USER):
    """Fetch repository issue comments."""
    url = (
        f'{GITHUB_API}/repos/{user}/{repo}/issues'
        f'/{number_issue}/comments'
    )
    return fetch_from_github(url)


def fetch_reviews_for_repo_pr(repo, number_pr, user=DEFAULT_USER):
    """Fetch repository pr reviews."""
    url = (
        f'{GITHUB_API}/repos/{user}/{repo}/pulls'
        f'/{number_pr}/comments'
    )
    return fetch_from_github(url)


def fetch_from_github(url, additional_params=None):
    """Fetch data from github api."""
    request_params = {PAGE_KEY: 1}
    request_params.update(additional_params or {})
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()

    pages = 1
    if response.links.get('last'):
        pages = get_count_pages(response.links['last']['url'])

    while request_params[PAGE_KEY] <= pages:
        response = requests.get(
            url,
            headers=get_headers(),
            params=request_params,
        )
        response.raise_for_status()
        request_params[PAGE_KEY] += 1
        yield from response.json()


def get_user_by_prs(prs):
    """Return user by user pr's."""
    return get_user_by_characteristic(prs, 'user')


def get_user_by_commits(commits):
    """Return user by user commits."""
    return get_user_by_characteristic(commits, 'author')


def get_user_by_characteristic(characteristic, look_up):
    """Return user by characteristics."""
    user_by_characteristic = {}
    for ch in characteristic:
        user = ch.get(look_up)
        if not user:
            continue
        login = user.get('login')
        user_by_characteristic[login] = (
            user_by_characteristic.get(login, 0) + 1
        )
    return user_by_characteristic


def get_count_pages(url):  # noqa: D103
    return int(parse_qs(urlparse(url).query)[PAGE_KEY][0])


def get_headers():
    """Return github auth header."""
    return {
        'Authorization': f'token {settings.GITHUB_AUTH_TOKEN}',
    }


def merge_dicts(*dicts):
    """Merges several dictionaries into one."""
    counter = Counter()
    for dict_ in dicts:
        counter.update(dict_)
    return counter


def get_commit_stats_for_contributor(repo_full_name, contributor_id):
    """Returns numbers of commits, additions, deletions for contributor."""
    url = f'{GITHUB_API}/repos/{repo_full_name}/stats/contributors'
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    if response.status_code == requests.codes.no_content:
        raise NoContributorsError(
            "Nobody has contributed to this repository yet.",
        )

    try:
        contributor_stats = [
            stats for stats in response.json()
            if stats['author']['id'] == contributor_id
        ][0]
    except IndexError:
        raise ContributorNotFoundError(
            "No such contributor in this repository.",
        )

    totals = merge_dicts(*contributor_stats['weeks'])

    return totals['c'], totals['a'], totals['d']


def get_name_of_contributor(url):
    """Returns a contributor's name."""
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()['name']
