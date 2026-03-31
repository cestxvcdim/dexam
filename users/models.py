import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


def generate_username():
    return str(uuid.uuid4())


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        default=generate_username,
        validators=[UnicodeUsernameValidator()],
    )
    ru_login = models.CharField(verbose_name="Русский логин", max_length=16, unique=True)
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=17, unique=True)

    first_name = models.CharField(verbose_name="Имя", max_length=32)
    last_name = models.CharField(verbose_name="Фамилия", max_length=32)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["ru_login", "email", "phone"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
