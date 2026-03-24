from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import WorkerRegistrationForm
from .models import Worker, Task, TaskType

@login_required()
def index(request):

    tasks = Task.objects.all().count()
    workers = Worker.objects.all().count()
    task_types = TaskType.objects.all().count()

    context = {
        "tasks": tasks,
        "workers": workers,
        "task_types": task_types,
        "segment": "index",
    }

    return render(request, "tasks/index.html", context)


def register_view(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:login')
    else:
        form = WorkerRegistrationForm
    return render(request, 'accounts/register.html', {'form': form})