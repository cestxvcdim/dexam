from django.db import models
from django.conf import settings


class BookCard(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "На рассмотрении"
        APPROVED = "approved", "Одобрено"
        REJECTED = "rejected", "Отклонено"
        ARCHIVED = "archived", "Архив"

    class ActionType(models.TextChoices):
        GIVE = "give", "Готов поделиться"
        WANT = "want", "Хочу в свою библиотеку"

    class Binding(models.TextChoices):
        HARD = "hard", "Твердый"
        SOFT = "soft", "Мягкий"

    class Condition(models.TextChoices):
        PERFECT = "perfect", "Идеальное"
        NORMAL = "normal", "Нормальное"
        BAD = "bad", "Требует внимания"
        TERRIBLE = "terrible", "Годится чтобы подпирать ножку стола"

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="book_cards",
    )

    author = models.CharField(verbose_name="Автор", max_length=128)
    title = models.CharField(verbose_name="Название", max_length=128)

    action_type = models.CharField(verbose_name="Выберите пункт", max_length=10, choices=ActionType.choices)

    publisher = models.CharField(verbose_name="Издательство", max_length=128, blank=True)
    year = models.PositiveIntegerField(verbose_name="Год издания", null=True, blank=True)
    binding = models.CharField(verbose_name="Переплет", max_length=10, choices=Binding.choices)
    condition = models.CharField(verbose_name="Состояние книги", max_length=20, choices=Condition.choices)

    status = models.CharField(
        verbose_name="Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        verbose_name = "Карточка книги"
        verbose_name_plural = "Карточки книг"

    def __str__(self):
        return f"{self.title} — {self.author}"
