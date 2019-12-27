from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


"""
View 'register' is responsible for:
 1) HTTP GET: getting access to register page;
 2) HTTP POST: creating new user in table User in DB according to data from a custom registration form.
"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


"""
View 'profile' is reposible for user's page.
Decorator @login_required checks if user is logged in before giving access to a profile.
"""
@login_required
def profile(request):
    return render(request, 'users/profile.html')


