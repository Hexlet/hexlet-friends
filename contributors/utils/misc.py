import os
from collections import Counter

from django.core.exceptions import ImproperlyConfigured
from django.db import models


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
