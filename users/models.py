from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(verbose_name="Логин", max_length=150, unique=True)
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    phone = models.CharField(verbose_name="Номер телефона", max_length=17, unique=True)
    full_name = models.CharField(verbose_name="ФИО", max_length=128)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone", "full_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
