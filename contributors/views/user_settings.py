from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from auth.forms import UserTokenForm
from contributors.views.mixins import (
    AuthRequiredMixin,
    PermissionRequiredMixin,
)


class ChangeTokenView(
    AuthRequiredMixin,
    PermissionRequiredMixin,
    TemplateView,
):
    """Changing user git_hub token page view."""

    template_name = "contributor/user_settings.html"
    not_auth_msg = _("Please log in with your GitHub")
    no_permission_msg = _("You haven't got permission to access this section")
    redirect_url = reverse_lazy("contributors:home")

    def get_context_data(self, **kwargs):
        """Add additional context for the settings."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission."""
        form = UserTokenForm(request.POST)
        if form.is_valid():
            user = request.user
            github_token = form.cleaned_data["github_token"]
            user.github_token = github_token
            user.save()
            messages.success(request, _("GitHub token changed successfully"))
            return redirect(
                reverse_lazy(
                    "contributors:user_settings",
                    kwargs={"slug": kwargs.get("slug")},
                )
            )

        messages.error(request, _("An error occurred. Please try again"))
        return redirect(
            reverse_lazy(
                "contributors:user_settings",
                kwargs={"slug": kwargs.get("slug")},
            )
        )
