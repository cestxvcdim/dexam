from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.mixins import StyleFormMixin

from users.models import User
from users.validators import (
    validate_full_name,
    validate_phone,
    validate_username,
)


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "full_name",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validate_username(username)
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").replace(" ", "")
        validate_phone(phone)
        return phone

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name", "").strip()
        validate_full_name(full_name)
        return full_name


class LoginForm(StyleFormMixin, AuthenticationForm):
    username = forms.CharField(label="Логин")

    error_messages = {
        "invalid_login": "Неверный логин или пароль.",
        "inactive": "Учётная запись отключена.",
    }
