from django.contrib.auth.backends import BaseBackend

from auth.models import SiteUser
from contributors.utils.misc import split_full_name


class GitHubBackend(BaseBackend):
    """GitHub auth."""

    def authenticate(self, request, user_data):
        """Authenticate the user."""
        login = user_data['login']
        try:
            user = SiteUser.objects.get(username=login)
        except SiteUser.DoesNotExist:
            email = user_data.get('email')
            first_name, last_name = split_full_name(user_data.get('name'))
            user = SiteUser.objects.create_user(
                username=login,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
        return user

    def get_user(self, user_id):
        """Return a user instance if it exists."""
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None
