from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count

from .forms import (
    WorkerRegistrationForm,
    WorkerSearchForm,
    TaskSearchForm,
    TaskCreationForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    TaskUpdateForm,
    PositionSearchForm,
)
from .models import Worker, Task, TaskType, Position


@login_required()
def index(request):
    num_active_tasks = Task.objects.filter(is_completed=False).count()
    tasks = Task.objects.all().count()
    workers = Worker.objects.all().count()
    task_types = TaskType.objects.all().count()
    unique_positions = Position.objects.all().count()
    popular_type = TaskType.objects.annotate(
        tasks_count=Count("tasks")
    ).order_by("-tasks_count").first()

    context = {
        "tasks": tasks,
        "num_active_tasks": num_active_tasks,
        "workers": workers,
        "unique_positions": unique_positions,
        "task_types": task_types,
        "segment": "index",
        "popular_type": popular_type.name if popular_type else "None",
    }
    return render(request, "tasks/index.html", context)


def register_view(request):
    if request.method == "POST":
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:login")
    else:
        form = WorkerRegistrationForm
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    def form_valid(self, form):
        remember_me = self.request.POST.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(None)
        return super().form_valid(form)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = TaskSearchForm(self.request.GET or None)
        if form.is_valid():
            qs = qs.filter(name__icontains=form.cleaned_data["name"])
        return qs


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "tasks/worker_detail.html"
    queryset = (Worker.objects.all()
                .select_related("position").prefetch_related("tasks"))


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "tasks/worker_create.html"

    def test_func(self):
        user = self.request.user
        return (user.is_superuser
                or (user.position and user.position.can_create_worker))

    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class WorkerUpdateView(LoginRequiredMixin,
                       UserPassesTestMixin,
                       generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "tasks/worker_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        worker = self.get_object()

        return self.request.user == worker or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy(
            "tasks:worker-list", kwargs={"pk": self.object.pk})


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "tasks/task_create.html"
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("tasks:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_create.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_update.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("tasks:task-type-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        form = PositionSearchForm(self.request.GET or None)
        if form.is_valid():
            qs = qs.filter(name__icontains=form.cleaned_data["name"])
        return qs


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "tasks/position_create.html"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "tasks/position_update.html"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
