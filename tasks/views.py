from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (WorkerRegistrationForm,
                    WorkerSearchForm,
                    TaskSearchForm,
                    TaskTypeSearchForm,
                    TaskCreationForm,
                    WorkerCreationForm,
                    )
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

class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(
            self, **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = WorkerSearchForm(self.request.GET or None)
        if form.is_valid():
            qs = qs.filter(username__icontains=form.cleaned_data["username"])
        return qs

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(
            self, **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = TaskSearchForm(self.request.GET or None)
        if form.is_valid():
            qs = qs.filter(model__icontains=form.cleaned_data["name"])
        return qs

class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5

    def get_context_data(
            self, **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskTypeSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = TaskSearchForm(self.request.GET or None)
        if form.is_valid():
            qs = qs.filter(model__icontains=form.cleaned_data["name"])
        return qs

class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "tasks/worker_detail.html"
    queryset = Worker.objects.all().select_related("position").prefetch_related("tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm

    def test_func(self):
        user = self.request.user
        return user.is_superuser or (user.position and user.position.can_create_worker)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks:task-list")

class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    pass