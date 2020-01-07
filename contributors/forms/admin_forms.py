from django import forms
from django.utils.translation import gettext_lazy as _
from requests.exceptions import HTTPError

from contributors.utils.github_lib import get_org_data


class OrgNamesForm(forms.Form):
    """A form for organization names."""

    organizations = forms.CharField(
        label=_("Organizations"),
        widget=forms.Textarea({'cols': 30, 'rows': 5}),
        help_text=_(
            "Enter organization names separated by a space or newline.",
        ),
    )

    def clean_organizations(self):
        """Check if valid names have been provided."""
        organizations = self.cleaned_data.get('organizations')
        for name in organizations.split():
            try:
                get_org_data(name)
            except HTTPError:
                raise forms.ValidationError(
                    _("Invalid name: ") + name,
                    code='invalid',
                    params={'name': name},
                )
        return organizations


class RepoNamesForm(forms.Form):
    """A form for repository names."""

    def __init__(self, *args, choices=None, **kwargs):
        """Initialize the form with a dynamic choices set."""
        super().__init__(*args, **kwargs)
        self.fields['repositories'] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=choices or {},
            help_text=_("Uncheck those you wish to skip."),
        )
