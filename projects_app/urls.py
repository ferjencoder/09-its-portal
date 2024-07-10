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
    path(
        "admin_dashboard/",
        views.admin_projects_dashboard,
        name="admin_projects_dashboard",
    ),
    path(
        "employee_dashboard/",
        views.employee_projects_dashboard,
        name="employee_projects_dashboard",
    ),
    path(
        "client_dashboard/",
        views.client_projects_dashboard,
        name="client_projects_dashboard",
    ),
    path("submit_feedback/", views.submit_feedback, name="submit_feedback"),
    path(
        "tasks/<int:task_id>/update_status/",
        views.update_task_status,
        name="update_task_status",
    ),
    path("create_task/", views.create_task, name="create_task"),
    path("edit_task/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
    path(
        "documents/upload/<int:deliverable_id>/",
        views.upload_document,
        name="upload_document",
    ),
    path(
        "documents/create_deliverable/<int:project_id>/",
        views.create_deliverable,
        name="create_deliverable",
    ),
    path(
        "documents/delete/<int:deliverable_id>/",
        views.delete_deliverable,
        name="delete_deliverable",
    ),
    path(
        "documents/approve/<int:document_id>/",
        views.approve_document,
        name="approve_document",
    ),
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    path(
        "deliverables/edit/<int:deliverable_id>/",
        views.edit_deliverable,
        name="edit_deliverable",
    ),
    path("create_update/", views.create_update, name="create_update"),
    path("add_document/", views.add_document, name="add_document"),
]
