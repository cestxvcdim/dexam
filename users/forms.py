import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from core.forms import StyleFormMixin
from users.models import User


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "ru_login",
            "email",
            "phone",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_ru_login(self):
        ru_login = self.cleaned_data.get("ru_login")

        if not re.match(r"^[А-Яа-яЁё0-9]+$", ru_login):
            raise ValidationError(
                "Логин должен содержать только кириллицу и цифры."
            )

        return ru_login

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        phone = phone.replace(" ", "")

        pattern = r"^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$"
        if not re.match(pattern, phone):
            raise ValidationError(
                "Телефон должен быть в формате +7(XXX)-XXX-XX-XX."
            )

        return phone


class LoginForm(StyleFormMixin, AuthenticationForm):
    username = forms.CharField(label="Логин")

    def clean(self):
        from django.contrib.auth import authenticate

        ru_login = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if ru_login and password:
            try:
                user = User.objects.get(ru_login=ru_login)
            except User.DoesNotExist:
                raise ValidationError("Пользователь не найден")

            self.user_cache = authenticate(
                self.request,
                username=user.username,
                password=password
            )

            if self.user_cache is None:
                raise ValidationError("Неверный пароль")

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
