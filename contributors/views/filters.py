import django_filters
from dateutil import relativedelta
from django import forms
from django.forms.widgets import TextInput
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from contributors.models import Contribution, ContributionLabel
from contributors.utils import misc

STATE_CHOICES = (
    ('open', _('Open')),
    ('closed', _('Closed')),
)

PERIOD_CHOICES = (
    ('for_week', _('For week')),
    ('for_month', _('For month')),
    ('for_year', _('For year')),
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

    class Meta:
        model = Contribution
        fields = [
            'info_title',
            'repository_full_name',
            'repository_labels',
            'info_state',
        ]

    def get_good_first_issue(self, queryset, name, value):
        """Filter issues by label 'good_first_issue'."""
        if value:  # Only apply filter if checkbox is checked
            good_first = ContributionLabel.objects.filter(
                name='good first issue',
            ).first()
            if good_first:
                queryset = queryset.filter(
                    labels__in=[good_first.id], info__state='open',
                )
        return queryset


class DetailTablePeriodFilter(django_filters.FilterSet):
    """Period contributions filter."""

    period = django_filters.ChoiceFilter(
        choices=PERIOD_CHOICES,
        widget=forms.Select,
        method='get_contributions_by_period',
        initial=None,
        label=_('Period'),
        field_name='period_filter',
    )

    def get_contributions_by_period(self, queryset, name, value):
        """Contributions filter for a period."""
        if value == 'for_year':
            datetime_now = timezone.now()
            date_eleven_months_ago = (
                datetime_now - relativedelta.relativedelta(
                    months=11, day=1,
                )
            ).date()
            queryset = queryset.filter(
                created_at__gte=date_eleven_months_ago,
            ).distinct()
        elif value == 'for_month':
            queryset = queryset.filter(
                created_at__gte=misc.datetime_month_ago(),
            ).distinct()
        elif value == 'for_week':
            queryset = queryset.filter(
                created_at__gte=misc.datetime_week_ago(),
            ).distinct()
        return queryset
