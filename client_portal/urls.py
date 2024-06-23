# client_portal/urls.py

from django.urls import path
from . import views


app_name = "client_portal"

urlpatterns = [
    path("", views.client_dashboard, name="client_dashboard"),
    path("dashboard/", views.client_dashboard, name="client_dashboard"),
    path("profile/", views.profile, name="client_profile"),
    path("profile/edit/", views.edit_profile, name="edit_client_profile"),
    path("projects/", views.view_projects, name="view_projects"),
    path("project/<int:id>/", views.project_detail, name="project_detail"),
]
