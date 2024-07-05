# projects_app/urls.py

from django.urls import path
from . import views

app_name = "projects_app"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("create/", views.create_project, name="create_project"),
    path("<int:project_id>/", views.view_project, name="view_project"),
    path(
        "<int:project_id>/update/",
        views.update_project_status,
        name="update_project_status",
    ),
    path("<int:project_id>/delete/", views.delete_project, name="delete_project"),
    path("view/", views.view_projects, name="view_projects"),
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/create/", views.create_assignment, name="create_assignment"),
]
