# projects_app/forms.py

from django.contrib.auth.models import User
from django import forms
from .models import Project, ProjectAssignment


class ProjectForm(forms.ModelForm):
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
            "description": forms.Textarea(attrs={"rows": 7}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["status"]


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = ["project", "employee", "client"]
