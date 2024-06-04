from contributors.views import (  # noqa: WPS235
    about,
    achievements,
    contributor_compare,
    home,
    landing,
    user_settings,
)
from contributors.views.contributors_views import (
    contributor,
    contributor_issues,
    contributor_prs,
    contributors,
    contributors_for_period,
)
from contributors.views.generic_list_views import (
    issues,
    leaderboards,
    pull_requests,
)
from contributors.views.organizations_views import organization, organizations
from contributors.views.projects_views import project, projects
from contributors.views.repositories_views import repositories, repository
from contributors.views.utils import config, filters, webhook
