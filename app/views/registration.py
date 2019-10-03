from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from app.forms import RegistrationForm

from django.contrib.auth.forms import UserCreationForm
class RegistrationView(CreateView):

    template_name = 'auth/registration.html'
    success_url = reverse_lazy('index')
    model = User
    form_class = RegistrationForm

    def form_valid(self, form):
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {
    #         'form': RegistrationForm()
    #     })
    # fields = ('username', 'email', 'password',)





