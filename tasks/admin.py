from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Task, TaskType, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):

    list_display = UserAdmin.list_display + ("position",)
    fieldsets = (UserAdmin.fieldsets
                 + (("Additional Info", {"fields": ("position",)}),))
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("position",)}),
    )


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display =\
        ("name", "deadline", "is_completed", "priority", "task_type")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "can_create_worker", "can_edit_tasks")
    search_fields = ["name"]
