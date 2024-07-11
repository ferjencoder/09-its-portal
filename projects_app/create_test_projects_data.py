# projects_app/create_test_projects_data.py

import os
import sys
import django
from django.utils.translation import gettext_lazy as _
from shutil import copyfile

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

# Path to the default document
default_document_path = os.path.join(
    project_root, "media", "project_files", "default_document.webp"
)


# Función para obtener usuarios existentes
def get_existing_users():
    clients = User.objects.filter(groups__name="client")
    employees = User.objects.filter(groups__name="employee")

    if not clients.exists() or not employees.exists():
        print(_("No se encontraron usuarios en los grupos 'client' o 'employee'."))
        return None, None

    return clients, employees


# Función para generar un código único de proyecto
def generate_unique_project_code(index):
    return f"AA{index:03}"


# Función para crear proyectos de prueba
def create_test_projects(clients, employees):
    projects = []
    for i in range(1, 6):
        client = clients[i % len(clients)]  # Loopea a través de los clientes
        employee = employees[i % len(employees)]  # Loopea a través de los empleados
        project_code = generate_unique_project_code(i)
        project = Project.objects.create(
            name=f"Project {i}",
            code=project_code,
            description=f"Esta es la descripción del Proyecto {i}.",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date(),
            status=choice([Project.PENDING, Project.ONGOING, Project.COMPLETED]),
            assigned_to_client=client,
        )
        project.assigned_to_employees.set([employee])
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


# Función para crear documentos de prueba con control de versiones
def create_test_documents(projects, employees, clients):
    documents = []
    for project in projects:
        for i in range(1, 6):
            # Crear documento original
            assigned_to = choice(employees.union(clients))
            folder = "entregados" if assigned_to in employees else "recibidos"
            document_path = os.path.join(
                "project_files", project.code, "documents", folder, f"doc_{i}.webp"
            )

            # Ensure the directory exists
            os.makedirs(
                os.path.dirname(os.path.join(project_root, "media", document_path)),
                exist_ok=True,
            )

            # Copy the default document to the new path
            copyfile(
                default_document_path,
                os.path.join(project_root, "media", document_path),
            )
            print(f"Documento {document_path} subido exitosamente.")

            document = Document.objects.create(
                project=project,
                name=f"Document {i} for {project.name}",
                file=document_path,
                status=choice(["pending", "uploaded"]),
                assigned_to=assigned_to,
                comments=f"Comentarios para el documento {i} de {project.name}.",
                version=1,
            )
            documents.append(document)

            # Crear versiones adicionales del documento original
            for v in range(2, 4):  # Crear 3 versiones por ejemplo
                document_version_path = os.path.join(
                    "project_files",
                    project.code,
                    "documents",
                    folder,
                    f"doc_{i}_v{v}.webp",
                )

                # Copy the default document to the new path
                copyfile(
                    default_document_path,
                    os.path.join(project_root, "media", document_version_path),
                )
                print(f"Documento {document_version_path} subido exitosamente.")

                document_version = Document.objects.create(
                    project=project,
                    name=f"Document {i} for {project.name} v{v}",
                    file=document_version_path,
                    status=choice(["pending", "uploaded"]),
                    assigned_to=assigned_to,
                    comments=f"Comentarios para el documento {i} versión {v} de {project.name}.",
                    version=v,
                    original_document=document,
                )
                documents.append(document_version)
    return documents


# Función para crear actualizaciones de prueba
def create_test_updates(projects):
    updates = []
    for project in projects:
        for i in range(1, 6):
            update = Update.objects.create(
                title=f"Actualización {i} para {project.name}",
                content=f"Contenido de la actualización {i} para {project.name}.",
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
        create_test_documents(projects, employees, clients)
        create_test_updates(projects)
        create_test_deliverables(projects, employees)
        print(_("Datos de prueba creados exitosamente."))
    else:
        print(
            _(
                "No se crearon datos de prueba debido a la falta de usuarios en los grupos especificados."
            )
        )


if __name__ == "__main__":
    main()
