from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from contributors.models import Organization


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


class OrganizationFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    organizations = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        label=_("Организации")
    )
