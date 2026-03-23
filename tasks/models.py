from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name="workers")

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        if self.position:
            position = self.position
        else:
            position = "no position"
        return (f"{self.username} "
                f"({self.first_name}"
                f" {self.last_name})"
                f"{position}")


class Priority(models.IntegerChoices):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"
    URGENT = 4, "Urgent"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False,
                                       db_index=True)
    priority = models.IntegerField(
        choices=Priority, default=Priority.MEDIUM)
    task_type = models.ForeignKey(TaskType,
                                  on_delete=models.CASCADE,
                                  related_name="tasks")
    assignees = models.ManyToManyField(Worker,
                                       related_name="tasks")


    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return (f"{self.name}"
                f" ({self.task_type.name}"
                f" | {self.get_priority_display()})")

