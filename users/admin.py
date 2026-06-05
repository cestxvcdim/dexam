from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = ("id", "username", "email", "phone", "first_name", "last_name")
    search_fields = ("username", "email", "phone", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
