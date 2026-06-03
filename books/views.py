from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from books.models import BookCard
from books.forms import BookCardForm, BookCardStatusForm
from books.mixins import StaffRequiredMixin


class BookCardCreateView(LoginRequiredMixin, CreateView):
    model = BookCard
    form_class = BookCardForm
    template_name = "books/create.html"
    success_url = reverse_lazy("books:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookCardListView(LoginRequiredMixin, ListView):
    model = BookCard
    template_name = "books/list.html"
    context_object_name = "book_cards"

    def get_queryset(self):
        return BookCard.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["active_book_cards"] = self.get_queryset().filter(
            status__in=("pending", "approved"),
        )
        context["archived_book_cards"] = self.get_queryset().filter(
            status__in=("rejected", "archived"),
        )

        return context

class BookCardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BookCard
    template_name = "books/detail.html"
    context_object_name = "book_card"

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.get_object().user == self.request.user
        )


class BookCardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookCard
    template_name = "books/delete.html"
    success_url = reverse_lazy("books:list")

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.get_object().user == self.request.user
        )


class AdminBookCardListView(StaffRequiredMixin, ListView):
    model = BookCard
    template_name = "books/admin_panel.html"
    context_object_name = "book_cards"
    paginate_by = 20

    def get_queryset(self):
        return BookCard.objects.select_related("user").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = BookCard.Status.choices
        return context


class AdminBookCardStatusUpdateView(StaffRequiredMixin, View):
    def post(self, request, pk):
        book_card = get_object_or_404(BookCard, pk=pk)
        form = BookCardStatusForm(request.POST)

        if form.is_valid():
            book_card.status = form.cleaned_data["status"]
            book_card.save(update_fields=["status"])
            messages.success(request, f"Статус карточки «{book_card.title}» обновлён.")
        else:
            messages.error(request, "Некорректный статус.")

        return redirect("books:admin_panel")
