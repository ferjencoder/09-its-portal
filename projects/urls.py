# projects/urls.py

from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("projects/", views.project_list, name="project_list"),
    path("<int:pk>/", views.view_project, name="view_project"),
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/update/", views.update_project_status, name="update_project_status"),
    path("<int:pk>/delete/", views.delete_project, name="delete_project"),
    path("view/", views.view_projects, name="view_projects"),
    path("view/<int:project_id>/", views.view_project, name="view_project"),
    path(
        "update_status/<int:project_id>/",
        views.update_project_status,
        name="update_project_status",
    ),
]
