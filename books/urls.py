from django.urls import path
from books.views import (
    BookCardCreateView,
    BookCardListView,
    BookCardDetailView,
    BookCardDeleteView,
    AdminBookCardListView,
    AdminBookCardStatusUpdateView,
)

from books.apps import BooksConfig

app_name = BooksConfig.name

urlpatterns = [
    path("", BookCardListView.as_view(), name="list"),
    path("detail/<int:pk>/", BookCardDetailView.as_view(), name="detail"),
    path("create/", BookCardCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", BookCardDeleteView.as_view(), name="delete"),
    path("panel/", AdminBookCardListView.as_view(), name="admin_panel"),
    path("panel/<int:pk>/status/", AdminBookCardStatusUpdateView.as_view(), name="admin_status"),
]
