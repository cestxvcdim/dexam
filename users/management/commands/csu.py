from django.core.management import BaseCommand
from config.settings import SUPERUSER_USERNAME, SUPERUSER_PASSWORD, SUPERUSER_RU_LOGIN, SUPERUSER_EMAIL, SUPERUSER_PHONE

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            user = User.objects.create(
                username=SUPERUSER_USERNAME,
                ru_login=SUPERUSER_RU_LOGIN,
                first_name="Вадим",
                last_name="Владимиров",
                email=SUPERUSER_EMAIL,
                phone=SUPERUSER_PHONE,
                is_superuser=True,
                is_staff=True,
            )
            user.set_password(SUPERUSER_PASSWORD)
            user.save()
            print("Суперпользователь создан успешно!")
