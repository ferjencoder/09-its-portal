# its_admin/urls.py

from django.urls import path
from . import views

app_name = "its_admin"

urlpatterns = [
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("view_projects/", views.view_projects, name="view_projects"),
    path("create_project/", views.create_project, name="create_project"),
    path("edit_project/<int:project_id>/", views.edit_project, name="edit_project"),
]
