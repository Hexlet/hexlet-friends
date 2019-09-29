import requests
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from collections import Counter


def fetch_all_repos_for_user(user='Hexlet'):
    url = f'https://api.github.com/users/{user}/repos'
    return fetch_from_github(url)


def fetch_commits_for_repo(repo, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/commits'
    return fetch_from_github(url)


def fetch_pr_for_repo(repo, user='Hexlet'):
    url = f'https://api.github.com/repos/{user}/{repo}/pulls'
    params = {'state': 'closed'}
    return fetch_from_github(url, params)


def fetch_from_github(url, advanced_params=None):
    params = {'page': 1}
    if advanced_params:
        params.update(advanced_params)
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


def get_user_by_prs(prs):
    user_by_prs = {}
    for pr in prs:
        if not pr.get('user'):
            continue
        login = pr['user']['login']
        user_by_prs[login] = user_by_prs[login] + 1 if user_by_prs.get(login, False) else 1
    return user_by_prs


def get_user_by_commits(commits):
    user_by_commits = {}
    for commit in commits:
        if not commit.get('author'):
            continue
        login = commit['author']['login']
        user_by_commits[login] = user_by_commits[login] + 1 if user_by_commits.get(login, False) else 1
    return user_by_commits


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
