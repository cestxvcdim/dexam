from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class AdminUser(UserAdmin):
    list_display = ('id', 'ru_login', 'email', 'phone', 'first_name', 'last_name')
    search_fields = ('ru_login', 'email', 'phone', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    paginate_by = 10
