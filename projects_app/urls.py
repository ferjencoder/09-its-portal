# projects_app/urls.py

from django.urls import path
from . import views

app_name = "projects_app"

urlpatterns = [
    # Lista de proyectos
    path("", views.project_list, name="project_list"),
    # Crear nuevo proyecto
    path("create/", views.create_project, name="create_project"),
    # Ver detalles del proyecto
    path("<int:project_id>/", views.view_project, name="view_project"),
    # Actualizar estado del proyecto
    path(
        "<int:project_id>/update/",
        views.update_project_status,
        name="update_project_status",
    ),
    # Eliminar proyecto
    path("<int:project_id>/delete/", views.delete_project, name="delete_project"),
    # Ver todos los proyectos
    path("view/", views.view_projects, name="view_projects"),
    # Lista de asignaciones
    path("assignments/", views.assignment_list, name="assignment_list"),
    # Crear nueva asignación de proyecto
    path("assignments/create/", views.create_assignment, name="create_assignment"),
    # Tablero de proyectos para administradores
    path(
        "admin_dashboard/",
        views.admin_projects_dashboard,
        name="admin_projects_dashboard",
    ),
    # Tablero de proyectos para empleados
    path(
        "employee_dashboard/",
        views.employee_projects_dashboard,
        name="employee_projects_dashboard",
    ),
    # Enviar feedback
    path("submit_feedback/", views.submit_feedback, name="submit_feedback"),
    # Actualizar estado de la tarea
    path(
        "tasks/<int:task_id>/update_status/",
        views.update_task_status,
        name="update_task_status",
    ),
    # Cargar documento para un entregable específico
    path(
        "documents/upload/<int:deliverable_id>/",
        views.upload_document,
        name="upload_document",
    ),
    # Crear nuevo entregable para un proyecto
    path(
        "documents/create_deliverable/<int:project_id>/",
        views.create_deliverable,
        name="create_deliverable",
    ),
    # Eliminar entregable
    path(
        "documents/delete/<int:deliverable_id>/",
        views.delete_deliverable,
        name="delete_deliverable",
    ),
    # Aprobar documento
    path(
        "documents/approve/<int:deliverable_id>/",
        views.approve_document,
        name="approve_document",
    ),
    # Editar proyecto
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    # Editar entregable
    path(
        "deliverables/edit/<int:deliverable_id>/",
        views.edit_deliverable,
        name="edit_deliverable",
    ),
]
