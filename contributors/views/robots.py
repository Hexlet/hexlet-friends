from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def render_to_response(self, context, **response_kwargs):
        template = loader.get_template(self.template_name)
        response = HttpResponse(
            template.render(context, self.request),
            content_type=self.content_type
        )
        return response
