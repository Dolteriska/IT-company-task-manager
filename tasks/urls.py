from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import (
    index,
    register_view,
    WorkerListView,
    WorkerDetailView,
    TaskListView,

)


urlpatterns = [
    path("", index, name="index"),
    path("register/", register_view, name="register"),
    path("accounts/login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),

               ]

app_name = "tasks"
