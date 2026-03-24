from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import index, register_view

urlpatterns = [
    path("", index, name="index"),
    path("register/", register_view, name="register"),
    path("accounts/login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),

               ]

app_name = "tasks"
