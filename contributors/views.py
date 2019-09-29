from django.views.generic import ListView

from contributors.models import Contributor


class ContributorsListView(ListView):
    model = Contributor
