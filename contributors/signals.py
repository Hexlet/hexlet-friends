import subprocess  # noqa: S404

from django.apps import apps

from contributors.utils import misc


def handle_user_post_save(sender, **kwargs):
    """Tie a user with a contributor profile."""
    site_user = kwargs['instance']

    if site_user.has_usable_password():
        # The user has registered with the default backend
        return

    if kwargs['created']:
        contributor, _ = misc.update_or_create_record(
            apps.get_model('contributors.Contributor'),
            misc.get_contributor_data(site_user.username),
        )
        contributor.user = site_user
        contributor.save()

        fetch_command = ['./manage.py', 'fetchdata', site_user.username]
        subprocess.Popen(fetch_command)  # noqa: S603
