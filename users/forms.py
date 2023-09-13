from django.contrib.auth import forms as auth_forms
from django import forms
from users.models import User
from service.forms import StyleFormMixin


class UserRegisterForm(StyleFormMixin, auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
