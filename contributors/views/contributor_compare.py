from django.db.models import Count, Q
from django.views.generic import ListView

from contributors.models import Contribution, Contributor, Repository
from contributors.views.filters import DetailTablePeriodFilter


class CompareWithYourselfView(ListView):
    """View of comparing current user with another one."""

    model = Contribution
    template_name = ('contributors_sections/'
                     'contributors/contributor_compare_with_yourself.html')
    slug_field = 'contributor'

    def get_queryset(self):
        """Override method for good queryset."""
        qs_enemy = Contribution.objects.filter(
            contributor=Contributor.objects.filter(
                login=self.request.path.split('/')[-2],
            ).first(),
        )
        qs_me = Contribution.objects.filter(
            contributor=Contributor.objects.get(login=self.request.user),
        )
        return qs_enemy | qs_me

    def get_context_data(self, **kwargs):
        """Adding filter and data to context data."""
        context = super().get_context_data(**kwargs)
        context['enemy_obj'] = Contributor.objects.filter(
            login=self.request.path.split('/')[-2],
        ).first()
        context['filter'] = DetailTablePeriodFilter(
            self.request.GET,
            queryset=self.get_queryset(),
        )

        me_qs = context['filter'].qs.filter(
            contributor=Contributor.objects.get(login=self.request.user),
        )
        context['me'] = me_qs.aggregate(
            commits=Count('id', filter=Q(type='cit')),
            pull_requests=Count('id', filter=Q(type='pr')),
            issues=Count('id', filter=Q(type='iss')),
            comments=Count('id', filter=Q(type='cnt')),
        )
        me_top_repo_with_counter = me_qs.values('repository').annotate(
            count=Count('repository'),
        ).order_by('-count').first()
        if me_top_repo_with_counter:
            me_top_repo_pk = me_top_repo_with_counter['repository']
            me_repo_full_name = Repository.objects.filter(
                pk=me_top_repo_pk,
            ).first().full_name
            context['me_top_repo'] = me_repo_full_name
        else:
            context['me_top_repo'] = '---'

        enemy_qs = context['filter'].qs.filter(
            contributor=context['enemy_obj'].pk,
        )
        context['enemy'] = enemy_qs.aggregate(
            commits=Count('id', filter=Q(type='cit')),
            pull_requests=Count('id', filter=Q(type='pr')),
            issues=Count('id', filter=Q(type='iss')),
            comments=Count('id', filter=Q(type='cnt')),
        )
        enemy_top_repo_with_counter = enemy_qs.values('repository').annotate(
            count=Count('repository'),
        ).order_by('-count').first()
        if enemy_top_repo_with_counter:
            enemy_top_repo_pk = enemy_top_repo_with_counter['repository']
            enemy_repo_full_name = Repository.objects.filter(
                pk=enemy_top_repo_pk,
            ).first().full_name
            context['enemy_top_repo'] = enemy_repo_full_name
        else:
            context['enemy_top_repo'] = '---'
        return context
