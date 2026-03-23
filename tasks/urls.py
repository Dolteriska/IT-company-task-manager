from django.urls import path

from .views import index

urlpatterns = [path("", index, name="custom-index")]

app_name = "tasks"
