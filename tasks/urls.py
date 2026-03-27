from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import (
    index,
    register_view,
    WorkerListView,
    WorkerDetailView,
    TaskCreateView,
    TaskListView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    WorkerUpdateView,

)


urlpatterns = [
    path("", index, name="index"),
    path("register/", register_view, name="register"),
    path("accounts/login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task_types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task_types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task_types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),

               ]

app_name = "tasks"
