from django.contrib import admin

from books.models import BookCard


@admin.register(BookCard)
class BookCardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "user", "created_at")
    search_fields = ("title", "author", "publisher", "year")
    list_filter = ("title", "author", "publisher", "year", "book_type", "binding", "condition")
    paginate_by = 10
