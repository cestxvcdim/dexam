from django import forms

from core.forms import StyleFormMixin
from books.models import BookCard


class BookCardForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BookCard
        fields = [
            "author",
            "title",
            "action_type",
            "publisher",
            "year",
            "binding",
            "condition",
        ]

        widgets = {
            "action_type": forms.RadioSelect,
            "binding": forms.Select,
            "condition": forms.Select,
        }


class BookCardStatusForm(forms.Form):
    status = forms.ChoiceField(
        label="Статус",
        choices=BookCard.Status.choices,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )
