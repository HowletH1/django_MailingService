from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from users import forms
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('service:main')

    def get_object(self, queryset=None):
        return self.request.user
