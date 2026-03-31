from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from users.forms import RegisterForm, LoginForm


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "users/login.html"
    success_url = "/"
