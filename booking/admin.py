from django.contrib import admin

from booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "start_date", "payment_method", "status", "user", "created_at")
    list_filter = ("status", "payment_method", "room")
    search_fields = ("user__username", "user__email")
