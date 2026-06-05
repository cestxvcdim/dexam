import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if len(value) < 6:
        raise ValidationError("Логин должен содержать не менее 6 символов.")

    username_pattern = re.compile(r"^[a-zA-Z0-9]+$")
    if not username_pattern.match(value):
        raise ValidationError(
            "Логин должен содержать только латинские буквы и цифры."
        )


def validate_phone(value):
    phone = value.replace(" ", "")
    phone_pattern = re.compile(r"^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$")
    if not phone_pattern.match(phone):
        raise ValidationError(
            "Телефон должен быть в формате +7(XXX)-XXX-XX-XX."
        )


def validate_full_name(value):
    full_name = value.strip()

    if len(full_name) < 3:
        raise ValidationError("ФИО должно содержать не менее 3 символов.")

    full_name_pattern = re.compile(r"^[А-Яа-яЁё\s\-]+$")
    if not full_name_pattern.match(full_name):
        raise ValidationError(
            "ФИО должно содержать только кириллицу, пробелы и дефис."
        )
