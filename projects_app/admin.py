# projects_app/admin.py

from django.contrib import admin
from .models import Project, ProjectAssignment, Task, Document, Update, Deliverable

# guarda los models en la db
admin.site.register(Project)
admin.site.register(ProjectAssignment)
admin.site.register(Task)
admin.site.register(Document)
admin.site.register(Update)
admin.site.register(Deliverable)
