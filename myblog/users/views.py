from .forms import UserRegisterForm
from django.contrib.auth.models import User

from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from django.contrib import messages


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    extra_context = {'title': 'Profile'}
    login_url = 'users:login'


class Registration(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    extra_context = {'title': 'Registration'}

    def get_success_url(self):
        return reverse('users:login')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        messages.success(request, f'Account created for {username}')
        return super().post(request, *args, **kwargs)






























































