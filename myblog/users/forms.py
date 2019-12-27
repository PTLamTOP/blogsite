from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


"""
UserRegisterForm is a custom form for user registration with additional field email.
It is used for creating new user in table User in database according to class Meta.
"""
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']