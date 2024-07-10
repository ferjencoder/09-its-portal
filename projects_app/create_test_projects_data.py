# projects_app/create_test_projects_data.py

import os
import sys
import django
from django.utils.translation import gettext_lazy as _

# Configurar el directorio del proyecto y el módulo de configuración
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")

django.setup()

from django.contrib.auth.models import User, Group
from projects_app.models import Project, Task, Document, Update, Deliverable
from django.utils import timezone
from random import choice, randint
from datetime import timedelta


# Función para obtener usuarios existentes
def get_existing_users():
    clients = User.objects.filter(groups__name="client")
    employees = User.objects.filter(groups__name="employee")

    if not clients.exists() or not employees.exists():
        print(_("No se encontraron usuarios en los grupos 'client' o 'employee'."))
        return None, None

    return clients, employees


# Función para crear proyectos de prueba
def create_test_projects(clients, employees):
    projects = []
    for i in range(1, 6):
        project = Project.objects.create(
            name=f"Project {i}",
            code=f"AA{i:03}",
            description=f"Esta es la descripción del Proyecto {i}.",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
            status=choice([Project.PENDING, Project.ONGOING, Project.COMPLETED]),
            assigned_to_client=choice(clients),
        )
        project.assigned_to_employees.set(employees)
        projects.append(project)
    return projects


# Función para crear tareas de prueba
def create_test_tasks(projects, employees):
    tasks = []
    for project in projects:
        for i in range(1, 11):
            task = Task.objects.create(
                name=f"Task {i} for {project.name}",
                description=f"Descripción de tarea {i} para {project.name}.",
                due_date=(timezone.now() + timedelta(days=randint(1, 365))).date(),
                status=choice(["pending", "ongoing", "completed"]),
                assigned_to=choice(employees),
                project=project,
            )
            tasks.append(task)
    return tasks


# Función para crear documentos de prueba
def create_test_documents(projects, employees):
    documents = []
    for project in projects:
        for i in range(1, 6):
            document = Document.objects.create(
                project=project,
                name=f"Document {i} for {project.name}",
                file=f"documents/doc_{i}.pdf",
                status=choice(["pending", "uploaded"]),
                assigned_to=choice(employees),
                comments=f"Coentarios para el documento {i} de {project.name}.",
            )
            documents.append(document)
    return documents


# Función para crear actualizaciones de prueba
def create_test_updates(projects):
    updates = []
    for project in projects:
        for i in range(1, 6):
            update = Update.objects.create(
                title=f"Actualización {i} para {project.name}",
                content=f"Contentenido de la actualización {i} para {project.name}.",
                date=timezone.now(),
                status=choice(
                    [
                        Update.CRITICAL,
                        Update.INFORMATIVE,
                        Update.WARNING,
                        Update.RESOLVED,
                        Update.ANNOUNCEMENT,
                    ]
                ),
                project=project,
            )
            updates.append(update)
    return updates


# Función para crear entregables de prueba
def create_test_deliverables(projects, employees):
    deliverables = []
    for project in projects:
        for i in range(1, 6):
            deliverable = Deliverable.objects.create(
                project=project,
                name=f"Entregable {i} para {project.name}",
                due_date=(timezone.now() + timedelta(days=randint(1, 365))).date(),
                assigned_to=choice(employees),
                document=f"deliverable/del_{i}.pdf",
                status=choice(
                    [
                        "pending",
                        "uploaded",
                        "approved",
                        "commented",
                        "rejected",
                        "annulled",
                    ]
                ),
                comments=f"Comentarios del Entregable {i} de {project.name}.",
            )
            deliverables.append(deliverable)
    return deliverables


# Función principal para ejecutar todas las funciones de prueba
def main():
    clients, employees = get_existing_users()
    if clients and employees:
        projects = create_test_projects(clients, employees)
        create_test_tasks(projects, employees)
        create_test_documents(projects, employees)
        create_test_updates(projects)
        create_test_deliverables(projects, employees)
        print(_("Datos de prueba creados exitosamente."))
    else:
        print(
            _(
                "No se crearon datos de prueba debido a la falta de usuarios en los grupos especificados."
            )
        )


# Ejecutar la función principal
if __name__ == "__main__":
    main()
