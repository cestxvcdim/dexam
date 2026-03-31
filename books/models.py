from django.db import models
from django.conf import settings


class BookCard(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "На рассмотрении"
        APPROVED = "approved", "Одобрено"
        REJECTED = "rejected", "Отклонено"
        ARCHIVED = "archived", "Архив"

    class BookType(models.TextChoices):
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

    author = models.CharField(max_length=128)
    title = models.CharField(max_length=128)

    book_type = models.CharField(max_length=10, choices=BookType.choices)

    publisher = models.CharField(max_length=128, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    binding = models.CharField(max_length=10, choices=Binding.choices, blank=True)
    condition = models.CharField(max_length=20, choices=Condition.choices, blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Карточка книги"
        verbose_name_plural = "Карточки книг"

    def __str__(self):
        return f"{self.title} — {self.author}"
