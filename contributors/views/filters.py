import django_filters
from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from contributors.models import Contribution, ContributionLabel

STATE_CHOICES = (
    ('open', _('Open')),
    ('closed', _('Closed')),
)


class IssuesFilter(django_filters.FilterSet):
    """Issues filter."""

    info_title = django_filters.CharFilter(
        field_name='info__title',
        lookup_expr='icontains',
        label='',
        widget=TextInput(attrs={'placeholder': _('Title')}),
    )
    repository_full_name = django_filters.CharFilter(
        field_name='repository__full_name',
        lookup_expr='icontains',
        label='',
        widget=TextInput(attrs={'placeholder': _('Repository name')}),
    )
    repository_labels = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='repository__labels__name',
        label='',
        widget=TextInput(attrs={'placeholder': _('Language')}),
    )
    info_state = django_filters.ChoiceFilter(
        choices=STATE_CHOICES,
        lookup_expr='icontains',
        field_name='info__state',
        label='',
        empty_label=_('Status'),
    )

    good_first_issue_filter = django_filters.BooleanFilter(
        field_name='good_first_issue',
        method='get_good_first_issue',
        widget=forms.CheckboxInput,
        label='good first issue',
    )

    class Meta:  # noqa: WPS306
        model = Contribution
        fields = [
            'info_title',
            'repository_full_name',
            'repository_labels',
            'info_state',
        ]

    def get_good_first_issue(self, queryset, name, value):  # noqa: WPS110
        """Filter issues by label 'good_first_issue'."""
        good_first = ContributionLabel.objects.filter(
            name='good first issue',
        ).first()
        all_open_issues = Contribution.objects.filter(
            type='iss', info__state='open',
        )
        if good_first is None:
            queryset = all_open_issues.none()
        elif value:
            queryset = all_open_issues.filter(
                labels__in=[good_first.id],
            )
        return queryset
