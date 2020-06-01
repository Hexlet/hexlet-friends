import datetime
import os
from collections import Counter, deque
from functools import partial

from django.core.exceptions import ImproperlyConfigured
from django.db import models

NUM_OF_MONTHS_IN_A_YEAR = 12


def getenv(env_variable):
    """Return an environment variable or raises an exception."""
    try:
        return os.environ[env_variable]
    except KeyError:
        raise ImproperlyConfigured(
            f"The {env_variable} setting must not be empty.",
        )


def merge_dicts(*dicts):
    """Merge several dictionaries into one."""
    counter = Counter()
    for dict_ in dicts:
        counter.update(dict_)
    return counter


def get_or_create_record(model, github_resp, additional_fields=None):
    """
    Get or create a database record based on GitHub JSON object.

    Args:
        model -- a model or instance of a model
        github_resp -- GitHub data as a JSON object decoded to dictionary
        additional_fields -- fields to override

    """
    model_fields = {
        'Organization': {'name': github_resp.get('login')},
        'Repository': {'full_name': github_resp.get('full_name')},
        'Contributor': {
            'login': github_resp.get('login'),
            'avatar_url': github_resp.get('avatar_url'),
        },
    }
    defaults = {
        'name': github_resp.get('name'),
        'html_url': github_resp.get('html_url'),
    }
    if isinstance(model, models.Model):
        class_name = model.repository_set.model.__name__
        manager = model.repository_set
    elif issubclass(model, models.Model):
        class_name = model.__name__
        manager = model.objects
    else:
        raise TypeError("Improper type of model")

    defaults.update(model_fields[class_name])
    defaults.update(additional_fields or {})
    return manager.get_or_create(
        id=github_resp['id'],
        defaults=defaults,
    )


def group_contribs_by_months(months_with_contrib_sums):
    """
    Group a list of contributions by month.

    Take a list of dictionaries {type: <name>, month: <num>, count: <num>}.
    Return a 12-length dictionary where each key refers to a dictionary of
    contribution sums for the corresponding month.

    >>> months_with_contrib_sums = [
    ...     {'type': 'cit', 'month': 1, 'count': 10},
    ...     {'type': 'cit', 'month': 2, 'count': 20},
    ...     {'type': 'cnt', 'month': 1, 'count': 10},
    ... ]
    >>> group_contribs_by_months(months_with_contrib_sums)
    {1: {'cit': 10, 'cnt': 10}, 2: {'cit': 20}}
    """
    sums_of_contribs_by_months = {}
    for contrib in months_with_contrib_sums:
        month = sums_of_contribs_by_months.setdefault(contrib['month'], {})
        month[contrib['type']] = contrib['count']
    return sums_of_contribs_by_months


def get_rotated_sums_for_contrib(sums_of_contribs_by_months, contrib_type):
    """
    Return an array of 12 sums of contributions of the given type.

    Each position corresponds to a month.
    The collection is left-shifted by the numeric value of the current month.
    """
    month_numbers = range(1, NUM_OF_MONTHS_IN_A_YEAR + 1)
    current_month_number = datetime.date.today().month
    array = deque([
        sums_of_contribs_by_months.get(month_number, {}).get(contrib_type, 0)
        for month_number in month_numbers
    ])
    array.rotate(-current_month_number)
    return list(array)


def get_contrib_sums_distributed_over_months(sums_of_contribs_by_months):
    """
    Return shifted monthly sums for each contribution type.

    The collections end with the current month.
    """
    rotated_sums_by_months = partial(
        get_rotated_sums_for_contrib, sums_of_contribs_by_months,
    )
    return {
        'commits': rotated_sums_by_months('cit'),
        'pull_requests': rotated_sums_by_months('pr'),
        'issues': rotated_sums_by_months('iss'),
        'comments': rotated_sums_by_months('cnt'),
    }
