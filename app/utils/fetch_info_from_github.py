from collections import Counter, namedtuple
from urllib.parse import urlparse, parse_qs

import requests
from django.conf import settings


def fetch_organization_by_name(org='Hexlet'):
    url = f'https://api.github.com/orgs/{org}'
    return fetch_single_from_github(url)


def fetch_user_by_name(user='Hexlet'):
    url = f'https://api.github.com/users/{user}'
    return fetch_single_from_github(url)


def fetch_stats_by_repo(repo, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/stats/contributors'
    return fetch_single_from_github(url)


def fetch_all_repos_for_user(user='Hexlet'):
    url = f'https://api.github.com/users/{user}/repos'
    return fetch_list_from_github(url)


def fetch_commits_for_repo(repo, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/commits'
    return fetch_list_from_github(url)


def fetch_pr_for_repo(repo, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/pulls'
    params = {'state': 'closed'}
    return fetch_list_from_github(url, params)


def fetch_issues_for_repo(repo, user='Hexlet'):
    """
    GitHub's REST API v3 considers every pull request an issue,
    but not every issue is a pull request. For this reason,
    "Issues" endpoints may return both issues and pull requests in the response.
    You can identify pull requests by the pull_request key.

    Need filter(lambda x: x.get('pull_request', False), issues)
    """
    url = f'https://api.github.com/repos/{user}/{repo}/issues'
    params = {'state': 'all'}
    return fetch_list_from_github(url, params)


def fetch_comments_for_repo_issue(repo, number_issue, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/issues/{number_issue}/comments'
    return fetch_list_from_github(url)


def fetch_reviews_for_repo_pr(repo, number_pr, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/pulls/{number_pr}/comments'
    return fetch_list_from_github(url)


def fetch_list_from_github(url, additional_params=None):
    params = {'page': 1}
    params.update(additional_params or {})
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()

    pages = 1
    if response.links.get('last'):
        pages = get_count_pages(response.links['last']['url'])

    while params['page'] <= pages:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        params['page'] += 1
        yield from response.json()


def fetch_single_from_github(url):
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def get_user_by_prs(prs):
    return get_user_by_characteristic(prs, 'user')


def get_user_by_commits(commits):
    return get_user_by_characteristic(commits, 'author')


def get_user_by_issues(issues):
    return get_user_by_characteristic(issues, 'user')


def get_user_by_comments(issues):
    return get_user_by_characteristic(issues, 'user')


def get_user_by_characteristic(characteristic, look_up):
    Person = namedtuple('Person', ['user_id', 'login'])
    user_by_characteristic = {}
    for ch in characteristic:
        user = ch.get(look_up)
        if not user:
            continue
        login = user.get('login')
        user_id = user.get('id')
        key = Person(int(user_id), login)
        user_by_characteristic[key] = user_by_characteristic.get(key, 0) + 1
    return user_by_characteristic


def get_user_by_additions(stats):
    return get_user_by_stats(stats, 'a')


def get_user_by_deletions(stats):
    return get_user_by_stats(stats, 'd')


def get_user_by_stats(stats, field):
    Person = namedtuple('Person', ['user_id', 'login'])
    user_by_stats = {}
    for st in stats:
        user = st['author']
        key = Person(int(user['id']), user['login'])
        user_by_stats[key] = sum(int(week[field]) for week in st['weeks'])
    return user_by_stats


def get_count_pages(url):
    return int(parse_qs(urlparse(url).query)['page'][0])


def get_headers():
    return {
        'Authorization': f'token {settings.GITHUB_TOKEN}'
    }


def sum_dicts(*dicts):
    c = Counter()
    for d in dicts:
        c.update(d)
    return c
