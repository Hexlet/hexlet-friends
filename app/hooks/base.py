from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app.hooks.decorators import validate_request


@method_decorator(csrf_exempt, name='dispatch')
class BaseHook(View):
    http_method_names = ['get', 'post']
    greeting = 'Привет!'

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.greeting)