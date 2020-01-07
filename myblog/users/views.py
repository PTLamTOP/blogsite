from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse


class UserProfile(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    login_url = 'users/login.html'
    context_object_name = 'profile'

    def get_object(self):
        profile = get_object_or_404(User, username=self.kwargs['username'])
        print(profile)
        return profile


class Registration(FormView):
    template_name = 'users/register.html'
    http_method_names = ['get', 'post']
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')  # redirect to /login/ page

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)




























































