from app.models import Contribution, Contributor
from app.utils import fetch_info_from_github as github


def create_contributor(user_id, login):
    info_user = github.fetch_user_by_name(login)
    contributor, _ = Contributor.objects.get_or_create(
        pk=user_id,
        login=login,
        name=info_user['name'],
        html_url=info_user['html_url']
    )
    return contributor


def populate_db(user_by_field, repo, field):
    for user in user_by_field:
        contributor = create_contributor(user.user_id, user.login)
        repo.contributors.add(contributor)
        contribution = Contribution.objects.filter(
            repository=repo,
            contributor=contributor,
        )
        if contribution:
            contribution.update(**{field: user_by_field[user]})
        else:
            Contribution.objects.create(
                repository=repo,
                contributor=contributor,
                **{field: user_by_field[user]}
            )
