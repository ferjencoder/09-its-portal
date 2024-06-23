# its_admin/forms.py

from django import forms
from .models import Assignment, Project


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["name", "description", "assigned_to", "project", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
