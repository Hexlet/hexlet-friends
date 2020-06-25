from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Field, Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from contributors.utils.misc import prepare_choices


class ListSortAndSearchForm(forms.Form):
    """A form for sort and search."""

    sort = forms.ChoiceField(label=_("Sort by"), required=False)
    descending = forms.BooleanField(
        label=_("Descending"), initial=False, required=False,
    )
    search = forms.CharField(label=_("Search"), required=False)
    page = forms.IntegerField(
        widget=forms.HiddenInput(), initial=1, required=False,
    )

    def __init__(self, sortable_fields, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.fields['sort'].choices = prepare_choices(sortable_fields)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline my-3'
        self.helper.layout = Layout(
            Field('sort', 'descending', 'search'),
            ButtonHolder(
                Submit('', _("Apply")),
                HTML(
                    """
                    <a class="btn btn-light"
                    href="{0}" role="button">{1}</a>
                    """.format('{{ request.path }}', _("Reset")),
                ),
            ),
        )
