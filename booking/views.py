from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from booking.models import Booking
from booking.forms import BookingForm, BookingStatusForm, BookingReviewForm
from booking.mixins import StaffRequiredMixin


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking/create.html"
    success_url = reverse_lazy("booking:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking/list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context["active_bookings"] = queryset.exclude(
            status=Booking.Status.COMPLETED,
        )
        context["completed_bookings"] = queryset.filter(
            status=Booking.Status.COMPLETED,
        )

        return context


class BookingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Booking
    template_name = "booking/detail.html"
    context_object_name = "booking"

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.get_object().user == self.request.user
        )

    def post(self, request, *args, **kwargs):
        booking = self.get_object()

        if booking.user != request.user:
            messages.error(request, "Нельзя оставить отзыв к чужой заявке.")
            return redirect("booking:detail", pk=booking.pk)

        if not booking.can_write_review:
            messages.error(
                request,
                "Отзыв можно оставить только после изменения статуса администратором.",
            )
            return redirect("booking:detail", pk=booking.pk)

        if booking.reviews.exists():
            messages.error(request, "Отзыв к этой заявке уже оставлен.")
            return redirect("booking:detail", pk=booking.pk)

        form = BookingReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Отзыв сохранён.")
        else:
            messages.error(request, "Проверьте текст отзыва.")

        return redirect("booking:detail", pk=booking.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.object

        context["review"] = booking.reviews.first()
        if (
            booking.user == self.request.user
            and booking.can_write_review
            and not context["review"]
        ):
            context["review_form"] = BookingReviewForm()

        return context


class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = "booking/delete.html"
    success_url = reverse_lazy("booking:list")

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.get_object().user == self.request.user
        )


class AdminBookingListView(StaffRequiredMixin, ListView):
    model = Booking
    template_name = "booking/admin_panel.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        queryset = Booking.objects.select_related("user").order_by("-created_at")

        status = self.request.GET.get("status")
        payment = self.request.GET.get("payment")

        if status:
            queryset = queryset.filter(status=status)
        if payment:
            queryset = queryset.filter(payment_method=payment)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Booking.Status.choices
        context["payment_choices"] = Booking.PaymentMethod.choices
        context["current_status"] = self.request.GET.get("status", "")
        context["current_payment"] = self.request.GET.get("payment", "")
        return context


class AdminBookingStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        form = BookingStatusForm(request.POST)

        if form.is_valid():
            booking.status = form.cleaned_data["status"]
            booking.save(update_fields=["status"])
            messages.success(
                request,
                f"Статус заявки №{booking.pk} обновлён.",
            )
        else:
            messages.error(request, "Некорректный статус.")

        redirect_url = reverse("booking:admin_panel")
        params = []
        status_filter = request.POST.get("filter_status")
        payment_filter = request.POST.get("filter_payment")
        page = request.POST.get("page")

        if status_filter:
            params.append(f"status={status_filter}")
        if payment_filter:
            params.append(f"payment={payment_filter}")
        if page:
            params.append(f"page={page}")

        if params:
            redirect_url = f"{redirect_url}?{'&'.join(params)}"

        return redirect(redirect_url)
