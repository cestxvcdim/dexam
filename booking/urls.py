from django.urls import path

from booking.views import (
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    BookingDeleteView,
    AdminBookingListView,
    AdminBookingStatusUpdateView,
)
from booking.apps import BookingConfig

app_name = BookingConfig.name

urlpatterns = [
    path("", BookingListView.as_view(), name="list"),
    path("detail/<int:pk>/", BookingDetailView.as_view(), name="detail"),
    path("create/", BookingCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", BookingDeleteView.as_view(), name="delete"),
    path("panel/", AdminBookingListView.as_view(), name="admin_panel"),
    path("panel/<int:pk>/status/", AdminBookingStatusUpdateView.as_view(), name="admin_status"),
]
