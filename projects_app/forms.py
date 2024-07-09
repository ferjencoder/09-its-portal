# projects_app/forms.py

from django.contrib.auth.models import User
from django import forms
from .models import Project, ProjectAssignment, Deliverable, Update, Task, Document


class ProjectForm(forms.ModelForm):
    # Form para crear y editar proyectos
    assigned_to_client = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name="client"), required=False
    )
    assigned_to_employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name="employee"),
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "status",
            "assigned_to_client",
            "assigned_to_employees",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectStatusForm(forms.ModelForm):
    # Form para actualizar el estado del proyecto
    class Meta:
        model = Project
        fields = ["status"]


class AssignmentForm(forms.ModelForm):
    # Form para asignaciones de proyectos
    class Meta:
        model = ProjectAssignment
        fields = ["project", "employee", "client"]


class DeliverableForm(forms.ModelForm):
    # Form para el manejo de los entregables
    class Meta:
        model = Deliverable
        fields = ["name", "due_date", "status"]


class UpdateForm(forms.ModelForm):
    # Form para crear updates del proyecto
    class Meta:
        model = Update
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "due_date",
            "status",
            "assigned_to",
            "project",
            "is_personal",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["deliverable", "file", "status", "assigned_to"]
