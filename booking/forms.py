from django import forms

from core.mixins import StyleFormMixin
from booking.models import Booking, BookingReview


class BookingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("room", "start_date", "payment_method")

        widgets = {
            "room": forms.Select,
            "payment_method": forms.Select,
        }


class BookingStatusForm(StyleFormMixin, forms.Form):
    status = forms.ChoiceField(
        label="Статус",
        choices=Booking.Status.choices,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )


class BookingReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = ("body",)
        labels = {"body": "Отзыв"}
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
