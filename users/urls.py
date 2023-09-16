from django.urls import path
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users import views as custom_views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', custom_views.RegisterView.as_view(), name='register'),
    path('invalid_veryfi/', auth_views.TemplateView.as_view(template_name='users/invalid_veryfi.html'), name='invalid_veryfi'),
    path('verify_email/<uidb64>/<token>/', custom_views.EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', auth_views.TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('confirm_email_done/', auth_views.TemplateView.as_view(template_name='users/confirm_email_done.html'),
         name='confirm_email_done'),
    path('profile/', custom_views.UserUpdateView.as_view(), name='profile'),

   ]
