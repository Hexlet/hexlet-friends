from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from contributors.models.repository import Repository


class TableSortSearchForm(forms.Form):
    """A search form."""

    search = forms.CharField(label=False, required=False)
    sort = forms.CharField(
        label=False, widget=forms.HiddenInput(), required=False,
    )
    labels = forms.CharField(
        label=False, widget=forms.HiddenInput(), required=False,
    )

    @property
    def helper(self):
        """Control form attributes and its layout."""
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_class = 'd-flex'
        helper.layout = Layout(
            Field('sort'),
            Field('labels'),
            FieldWithButtons(
                Field('search', placeholder=_("Filter by name")),
                StrictButton(
                    _("Search"),
                    type='submit',
                    css_class='btn btn-outline-primary',
                ),
            ),
        )
        return helper


class CombinedSearchForm(TableSortSearchForm):
    """Search form of contributors by organization."""

    organizations = forms.CharField(
        label=False,
        required=False,
        widget=forms.TextInput(),
        help_text=_("Exact match required for this field"),
    )

    @property
    def helper(self):
        """Control form attributes and its layout."""
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_class = 'd-flex'
        helper.layout = Layout(
            Field('search', placeholder=_("Filter by name")),
            FieldWithButtons(
                Field(
                    'organizations', placeholder=_("Filter by organization"),
                ),
                StrictButton(
                    _("Search"),
                    type='submit',
                    css_class='btn btn-outline-primary',
                ),
            ),
        )
        return helper


class LeaderboardCombinedSearchForm(TableSortSearchForm):
    """Search form of contributors by organization."""

    organizations = forms.CharField(
        label=False,
        required=False,
        widget=forms.TextInput(),
        help_text=_("Exact match required for this field"),
    )

    sample = forms.ChoiceField(
        required=False,
        label='',
        choices=(
            ('all', _('All users')),
            ('except_staff', _('Except staff')),
            ('only_staff', _('Only staff')),
        ),
    )

    @property
    def helper(self):
        """Control form attributes and its layout."""
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_class = 'd-flex'
        helper.layout = Layout(
            Field('sample', placeholder='Sample'),
            Field('search', placeholder=_("Filter by name")),
            FieldWithButtons(
                Field(
                    'organizations',
                    placeholder=_("Filter by organization"),
                ),
                StrictButton(
                    _("Search"),
                    type='submit',
                    css_class='btn btn-outline-primary',
                ),
            ),
        )
        return helper


class NameStatusFilterForm(TableSortSearchForm):
    """Search form of issues by their status."""

    status_choices = [
        ('', _('Filter by status')),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    state = forms.ChoiceField(
        choices=status_choices,
        required=False,
        label=False,
        initial='',
    )

    repository = forms.ModelChoiceField(
        queryset=Repository.objects.all(),
        required=False,
        label=False,
        empty_label=_("Filter by repository"),
    )

    @property
    def helper(self):
        """Control form attributes and its layout."""
        helper = FormHelper()
        helper.form_method = 'get'
        helper.form_class = 'd-flex'
        helper.layout = Layout(
            Field('search', placeholder=_("Filter by name")),
            Field('state'),
            Field('repository'),
            Field('created_after'),
            FieldWithButtons(
                Field('created_till'),
                StrictButton(
                    _("Search"),
                    type='submit',
                    css_class='btn btn-outline-primary',
                ),
            ),
        )
        return helper


class PullRequestNameStatusFilterForm(NameStatusFilterForm):
    """Search form of pull requests by their status."""

    status_choices = [
        ('', _('Filter by status')),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('merged', 'Merged'),
    ]

    state = forms.ChoiceField(
        choices=status_choices,
        required=False,
        label=False,
        initial='',
    )
    created_till = forms.DateField(
        required=False,
        label=False,
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'placeholder': _("Created till"),
                'onfocus': "(this.type='date')",
            },
        ),
    )
    created_after = forms.DateField(
        required=False,
        label=False,
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'placeholder': _("Created after"),
                'onfocus': "(this.type='date')",
            },
        ),
    )
