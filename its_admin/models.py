# its_admin/models.py

from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="assignments"
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
