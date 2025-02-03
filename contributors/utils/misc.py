import os
from collections import deque
from functools import partial
from types import MappingProxyType

from dateutil import relativedelta
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

from contributors.utils import github_lib as github

NUM_OF_MONTHS_IN_A_YEAR = 12


def getenv(env_variable):
    """Return an environment variable or raise an exception."""
    try:
        return os.getenv(env_variable)
    except KeyError:
        raise ImproperlyConfigured(
            f"The {env_variable} setting must not be empty.",
        )


def update_or_create_record(cls, github_resp, additional_fields=None):
    """
    Update or create a database record based on a GitHub JSON object.

    Args:
        cls -- a class
        github_resp -- GitHub data as a JSON object decoded to dictionary
        additional_fields -- fields to override or add

    """
    cls_fields = {
        "Organization": lambda: {"name": github_resp["login"]},
        "Repository": lambda: {
            "owner_id": (
                github_resp["owner"]["id"]
                if github_resp["owner"]["type"] == "User"
                else None
            ),
            "organization_id": (
                github_resp["owner"]["id"]
                if github_resp["owner"]["type"] == "Organization"
                else None
            ),
            "full_name": github_resp["full_name"],
        },
        "Contributor": lambda: {
            "login": github_resp["login"],
            "avatar_url": github_resp["avatar_url"],
        },
    }
    defaults = {
        "name": github_resp.get("name"),
        "html_url": github_resp["html_url"],
    }

    defaults.update(cls_fields[cls.__name__]())
    defaults.update(additional_fields or {})
    return cls.objects.update_or_create(
        id=github_resp["id"],
        defaults=defaults,
    )


def get_contributor_data(login, session=None):
    """Get contributor data from database or GitHub."""
    Contributor = apps.get_model("contributors.Contributor")  # noqa: N806
    try:
        user = Contributor.objects.get(login=login)
    except Contributor.DoesNotExist:
        return github.get_owner_data(login, session)
    return {
        "id": user.id,
        "name": user.name,
        "html_url": user.html_url,
        "login": user.login,
        "avatar_url": user.avatar_url,
    }


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
        month = sums_of_contribs_by_months.setdefault(contrib["month"], {})
        month[contrib["type"]] = contrib["count"]
    return sums_of_contribs_by_months


def get_rotated_sums_for_contrib(
    current_month: int,
    sums_of_contribs_by_months,
    contrib_type,
):
    """
    Return an array of 12 sums of contributions of the given type.

    Each position corresponds to a month.
    The collection is left-shifted by the numeric value of the current month.
    """
    months = range(1, NUM_OF_MONTHS_IN_A_YEAR + 1)
    array = deque(
        [
            sums_of_contribs_by_months.get(month, {}).get(contrib_type, 0)
            for month in months
        ]
    )
    array.rotate(-current_month)
    return list(array)


def get_contrib_sums_distributed_over_months(
    current_month: int,
    sums_of_contribs_by_months,
):
    """
    Return shifted monthly sums for each contribution type.

    The collections end with the current month.
    """
    rotated_sums_by_months = partial(
        get_rotated_sums_for_contrib,
        current_month,
        sums_of_contribs_by_months,
    )
    return {
        "commits": rotated_sums_by_months("cit"),
        "pull_requests": rotated_sums_by_months("pr"),
        "issues": rotated_sums_by_months("iss"),
        "comments": rotated_sums_by_months("cnt"),
    }


def datetime_month_ago():
    """Return datetime 1 month ago from now."""
    dt_now = timezone.now()
    return dt_now - relativedelta.relativedelta(months=1)


def datetime_week_ago():
    """Return datetime 1 week ago from now."""
    dt_now = timezone.now()
    return dt_now - relativedelta.relativedelta(weeks=1)


def split_full_name(name):
    """Split a full name into parts."""
    if not name:
        return ("", "")
    name_parts = name.split()
    first_name = name_parts[0]
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    return (first_name, last_name)


def split_ordering(ordering):
    """Return a tuple of ordering direction and field name."""
    if ordering.startswith("-"):
        return ("-", ordering[1:])
    return ("", ordering)


DIRECTION_TRANSLATIONS = MappingProxyType(
    {
        "": "asc",
        "-": "desc",
    }
)
