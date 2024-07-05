# projects_app/admin.py

from django.contrib import admin
from .models import Project, ProjectAssignment

admin.site.register(Project)
admin.site.register(ProjectAssignment)
