from django.urls import path
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users import views as custom_views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', custom_views.RegisterView.as_view(), name='register'),
    path('profile/', custom_views.ProfileView.as_view(), name='profile'),


   ]
