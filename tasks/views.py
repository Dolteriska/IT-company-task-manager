from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Worker, Task


def index(request):

    tasks = Task.objects.select_related("task_type").all()

    context = {
        "tasks": tasks,
        "segment": "index",
    }

    return render(request, "pages/custom-index.html", context)
