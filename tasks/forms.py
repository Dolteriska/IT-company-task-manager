from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from tasks.models import Task

User = get_user_model()


class WorkerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }


class WorkerUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "position")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        optional_fields = ["first_name", "last_name", "email", "position"]
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False

        if self.user:
            is_admin = self.user.is_superuser
            can_manage = getattr(
                self.user.position,
                'can_create_worker',
                False) if self.user.position else False

            if not (is_admin or can_manage):
                if 'position' in self.fields:
                    self.fields['position'].disabled = True


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TaskUpdateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.select_related("position").all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input"}),
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 15}),
            "priority": forms.Select(
                attrs={"class": "form-control"}),
            "task_type": forms.Select(
                attrs={"class": "form-control"}),
            "is_completed": forms.CheckboxInput(
                attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            is_assigned = False
            if self.instance.pk:
                is_assigned = self.instance.assignees.filter(
                    pk=self.user.pk).exists()
            is_admin = self.user.is_superuser
            can_edit_all = (
                getattr(self.user.position, "can_edit_tasks", False)
                if self.user.position
                else False
            )
            if not (is_admin or can_edit_all):
                fields_to_disable = [
                    "name",
                    "description",
                    "deadline",
                    "priority",
                    "task_type",
                    "assignees",
                ]
                if not is_assigned:
                    fields_to_disable.append("is_completed")
                for field_name in fields_to_disable:
                    if field_name in self.fields:
                        self.fields[field_name].disabled = True
