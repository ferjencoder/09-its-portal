# projects_app/models.py

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    PENDING = "pending"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ONGOING, "Ongoing"),
        (COMPLETED, "Completed"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    assigned_to_client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_client_projects",
    )
    assigned_to_employees = models.ManyToManyField(
        User, blank=True, related_name="assigned_employee_projects"
    )

    def __str__(self):
        return self.name


class ProjectAssignment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="assignments"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_project_clients"
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_project_employees"
    )

    def __str__(self):
        return (
            f"{self.project.name} - {self.client.username} - {self.employee.username}"
        )