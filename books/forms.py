from django import forms
from core.forms import StyleFormMixin
from books.models import BookCard


class BookCardForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BookCard
        fields = [
            "author",
            "title",
            "book_type",
            "publisher",
            "year",
            "binding",
            "condition",
        ]

        widgets = {
            "book_type": forms.Select,
            "binding": forms.Select,
            "condition": forms.Select,
        }
