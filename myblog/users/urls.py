from django.urls import path, include
from django.contrib.auth import views
from .views import UserProfile, Registration


app_name = 'users'

urlpatterns = [
    path('register/', Registration.as_view(), name='register'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True,
                                           template_name='users/login.html',
                                           extra_context={'title': 'Login'}), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='users/logout.html',
                                             extra_context={'title': 'Logout'}), name='logout'),
    path('profile/<str:username>', UserProfile.as_view(), name='profile')
]