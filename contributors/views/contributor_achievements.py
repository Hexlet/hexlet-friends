from django.db import models
from django.db.models.functions import Coalesce
from django.views import generic

from contributors.models import Contributor, Repository

ID = 'id'


class ContributorAchievementListView(generic.ListView):
    """Achievement list."""

    template_name = 'contributor/contributor_achievements_list.html'
    model = Contributor
    contributors = Contributor.objects.with_contributions()

    pull_request_ranges_for_achievements = [1, 10, 25, 50, 100]
    commit_ranges_for_achievements = [1, 25, 50, 100, 200]
    issue_ranges_for_achievements = [1, 5, 10, 25, 50]
    comment_ranges_for_achievements = [1, 25, 50, 100, 200]
    edition_ranges_for_achievements = [1, 100, 250, 500, 1000]

    def get_context_data(self, **kwargs):
        """Add context data for achievement list."""
        self.contributors_amount = Contributor.objects.count()
        context = super().get_context_data(**kwargs)
        contributors = Contributor.objects.with_contributions()
        current_contributor = self._get_cur_contributor()
        repositories = self._get_repositories(current_contributor)
        contributions = self._aggregate_contributions(repositories)

        context.update(self._calculate_achievements(contributors, contributions))

        context['current_contributor'] = current_contributor
        context['contributors_amount'] = self.contributors_amount
        context['contributors_with_any_contribution'] = (
            self._contributors_with_any_contribution(contributors))
        return context

    def _get_cur_contributor(self):
        return Contributor.objects.get(login=self.kwargs['slug'])

    def _get_repositories(self, current_contributor):
        """Get repositories where the current contributor made contributions."""
        return Repository.objects.select_related(
            'organization',
        ).filter(
            is_visible=True,
            contribution__contributor=current_contributor,
        ).annotate(
            commits=models.Count('id', filter=models.Q(contribution__type='cit')),
            additions=Coalesce(models.Sum('contribution__stats__additions'), 0),
            deletions=Coalesce(models.Sum('contribution__stats__deletions'), 0),
            pull_requests=models.Count(
                'contribution', filter=models.Q(contribution__type='pr'),
            ),
            issues=models.Count(
                'contribution',
                filter=models.Q(contribution__type='iss')),
            comments=models.Count(
                'contribution',
                filter=models.Q(contribution__type='cnt')),
        ).order_by('organization', 'name')

    def _aggregate_contributions(self, repositories):
        """Aggregate all the contributions for the contributor."""
        return repositories.values().aggregate(
            contributor_deletions=models.Sum('deletions'),
            contributor_additions=models.Sum('additions'),
            contributor_commits=models.Sum('commits'),
            contributor_pull_requests=models.Sum('pull_requests'),
            contributor_issues=models.Sum('issues'),
            contributor_comments=models.Sum('comments'),
        )

    def _calculate_achievements(self, contributors, contributions):
        """Calculate achievements for various contribution types."""
        finished = []
        unfinished = []

        context = {
            'commits': contributions['contributor_commits'],
            'pull_requests': contributions['contributor_pull_requests'],
            'issues': contributions['contributor_issues'],
            'comments': contributions['contributor_comments'],
            'total_editions': self._calculate_editions(contributions),
            'total_actions': self._calculate_total_actions(contributions),
            'pull_request_ranges_for_achievements':
                self.pull_request_ranges_for_achievements,
        }

        # Process each type of achievement
        finished, unfinished = self._process_achievements(
            finished, unfinished, context, contributors, contributions
        )
        context['finished'] = finished
        context['unfinished'] = unfinished
        context['closed'] = len(finished)
        context['all_achievements'] = len(finished) + len(unfinished)
        return context

    def _process_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process all achievements types (pull request, commit, etc.)."""
        # Pull request achievements:
        finished, unfinished = self._process_pull_request_achievements(
            finished, unfinished, context, contributors, contributions
        )

        # Commit achievements:
        finished, unfinished = self._process_commit_achievements(
            finished, unfinished, context, contributors, contributions
        )

        # Issue achievements:
        finished, unfinished = self._process_issue_achievements(
            finished, unfinished, context, contributors, contributions
        )

        # Comment achievements:
        finished, unfinished = self._process_comment_achievements(
            finished, unfinished, context, contributors, contributions
        )

        # Edition achievements:
        finished, unfinished = self._process_edition_achievements(
            finished, unfinished, context, contributors, contributions
        )

        return finished, unfinished

    def _process_pull_request_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process achievements related to pull requests."""
        for pr_num in self.pull_request_ranges_for_achievements:
            context[f'contributors_pull_requests_gte_{pr_num}'] = {
                'stat': contributors.filter(pull_requests__gte=pr_num).count(),
                'acomplished':
                    self._get_cur_contributor() in contributors.filter(
                        pull_requests__gte=pr_num
                ),
            }
            a_data = self._create_achievement_data(
                pr_num, 'pull_requests', 'Pull requests'
            )
            finished, unfinished = self._update_achievement_status(
                pr_num,
                contributions['contributor_pull_requests'],
                a_data,
                finished,
                unfinished
            )
        return finished, unfinished

    def _process_commit_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process achievements related to commits."""
        for commit_num in self.commit_ranges_for_achievements:
            context[f'contributors_commits_gte_{commit_num}'] = {
                'stat': contributors.filter(commits__gte=commit_num).count(),
                'acomplished':
                    self._get_cur_contributor() in contributors.filter(
                        commits__gte=commit_num
                ),
            }
            a_data = self._create_achievement_data(
                commit_num, 'commits', 'Commits'
            )
            finished, unfinished = self._update_achievement_status(
                commit_num,
                contributions['contributor_commits'],
                a_data,
                finished,
                unfinished
            )
        return finished, unfinished

    def _process_issue_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process achievements related to issues."""
        for issue_num in self.issue_ranges_for_achievements:
            context[f'contributors_issues_gte_{issue_num}'] = {
                'stat': contributors.filter(issues__gte=issue_num).count(),
                'acomplished':
                    self._get_cur_contributor() in contributors.filter(
                        issues__gte=issue_num),
            }
            a_data = self._create_achievement_data(
                issue_num, 'issues', 'Issues'
            )
            finished, unfinished = self._update_achievement_status(
                issue_num,
                contributions['contributor_issues'],
                a_data,
                finished,
                unfinished
            )
        return finished, unfinished

    def _process_comment_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process achievements related to comments."""
        for comment_num in self.comment_ranges_for_achievements:
            context[f'contributors_comments_gte_{comment_num}'] = {
                'stat': contributors.filter(comments__gte=comment_num).count(),
                'acomplished':
                    self._get_cur_contributor() in contributors.filter(
                        comments__gte=comment_num),
            }
            a_data = self._create_achievement_data(
                comment_num, 'comments', 'Comments'
            )
            finished, unfinished = self._update_achievement_status(
                comment_num,
                contributions['contributor_comments'],
                a_data,
                finished,
                unfinished
            )
        return finished, unfinished

    def _process_edition_achievements(
        self, finished, unfinished, context, contributors, contributions
    ):
        """Process achievements related to code editions (additions + deletions)."""
        editions = self._calculate_editions(contributions)
        for ed_num in self.edition_ranges_for_achievements:
            context[f'contributors_editions_gte_{ed_num}'] = {
                'stat': contributors.filter(editions__gte=ed_num).count(),
                'acomplished':
                    self._get_cur_contributor() in contributors.filter(
                        editions__gte=ed_num),
            }
            a_data = self._create_achievement_data(
                ed_num, 'code_editions', 'Additions and deletions'
            )
            finished, unfinished = self._update_achievement_status(
                ed_num, editions, a_data, finished, unfinished
            )
        return finished, unfinished

    def _create_achievement_data(self, num, type_key, type_name):
        """Create achievement data dictionary."""
        return {
            'img': f'images/achievments_icons/{type_key}-{num}.svg',
            'name': f'{type_name} (equal to or more than {num})',
            'description':
                f"Make {type_name.lower()} in amount of equal to or more than {num}",
        }

    def _update_achievement_status(self, num, cur_value, a_data, finished, unfinished):
        """Update the achievement status."""
        if num > (0 if cur_value is None else cur_value):
            unfinished.append(a_data)
            a_data['acomplished'] = False
        else:
            finished.append(a_data)
        return finished, unfinished

    def _calculate_editions(self, contributions):
        """Calculate total editions (additions + deletions)."""
        return sum(
            0 if edit is None else edit
            for edit in [
                contributions['contributor_additions'],
                contributions['contributor_deletions'],
            ])

    def _calculate_total_actions(self, contributions):
        """Calculate total actions"""
        return sum(
            0 if action is None else action
            for action in [
                contributions['contributor_commits'],
                contributions['contributor_pull_requests'],
                contributions['contributor_issues'],
                contributions['contributor_comments'],
                contributions['contributor_additions'],
                contributions['contributor_deletions'],
            ])

    def _contributors_with_any_contribution(self, contributors):
        """Get the contributors with any contributions."""
        return {
            'stat': contributors.filter(contribution_amount__gte=1).count(),
            'acomplished': True,
        }
