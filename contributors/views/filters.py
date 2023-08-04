import django_filters
from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _

from contributors.models import Contribution, ContributionLabel


class IssuesFilter(django_filters.FilterSet):
    """Open issues filter."""

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
        ]

    def get_good_first_issue(self, queryset, name, value):  # noqa: WPS110
        """Filter open issues by label 'good_first_issue'."""
        good_first = ContributionLabel.objects.get(
            name='good_first_issue',
        )
        all_open_issues = Contribution.objects.filter(
            type='iss', info__state='open',
        )
        if value:
            queryset = all_open_issues.filter(
                labels__in=[good_first.id],
            )
        return queryset
