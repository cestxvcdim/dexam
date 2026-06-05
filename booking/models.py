from django.db import models
from django.conf import settings


class Booking(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        PLANNED = "planned", "Мероприятие назначено"
        COMPLETED = "completed", "Мероприятие завершено"

    class Room(models.TextChoices):
        AUDITORIUM = "auditorium", "Аудитория"
        COWORKING = "coworking", "Коворкинг"
        CINEMA = "cinema", "Кинозал"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Наличные"
        CARD = "card", "Банковская карта"

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    room = models.CharField(
        verbose_name="Помещение",
        max_length=16,
        choices=Room.choices,
    )
    start_date = models.DateTimeField(verbose_name="Дата начала конференции")
    payment_method = models.CharField(
        verbose_name="Способ оплаты",
        max_length=8,
        choices=PaymentMethod.choices,
    )

    status = models.CharField(
        verbose_name="Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на бронь"
        verbose_name_plural = "Заявки на бронь"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} {self.created_at}"

    @property
    def can_write_review(self):
        return self.status == self.Status.COMPLETED


class BookingReview(models.Model):
    booking = models.ForeignKey(
        verbose_name="Заявка на бронь",
        to=Booking,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    body = models.TextField(verbose_name="Содержимое")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв к заявке #{self.booking_id}"
