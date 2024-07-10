# projects_app/forms.py

from django.contrib.auth.models import User
from django import forms
from .models import Project, ProjectAssignment, Deliverable, Update, Task, Document


# Form para crear y editar proyectos
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


# Form para actualizar el estado del proyecto
class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["status"]


# Form para asignaciones de proyectos
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ["project", "employee", "client"]


# Form para el manejo de los entregables
class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ["name", "due_date", "status"]


# Form para crear updates del proyecto
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


# Form para crear tareas
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "due_date",
            "status",
            "project",
            "is_personal",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


# Form para cargar docs
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["project", "name", "file", "status", "assigned_to", "comments"]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 3}),
        }
