from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from books.models import BookCard
from books.forms import BookCardForm


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

        context["active_book_cards"] = self.get_queryset().exclude(
            status__in=("rejected", "archived"),
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
        return self.request.user.is_superuser or self.get_object().user == self.request.user


class BookCardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookCard
    template_name = "books/delete.html"
    success_url = reverse_lazy("books:list")

    def test_func(self):
        return self.request.user.is_superuser or self.get_object().user == self.request.user
