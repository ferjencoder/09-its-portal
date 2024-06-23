# its_admin/urls.py

from django.urls import path
from . import views

app_name = "its_admin"

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("create_assignment/", views.create_assignment, name="create_assignment"),
    path("create_project/", views.create_project, name="create_project"),
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("projects/", views.project_list, name="project_list"),
]
