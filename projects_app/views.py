# projects_app/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import BlogPost
from forum_app.models import ForumPost
from messages_app.models import Message
from .forms import ProjectForm, ProjectStatusForm, AssignmentForm
from .models import Project, ProjectAssignment, Task, Document, Update, Deliverable


# Verifica si el usuario es administrador
def is_admin(user):
    return user.groups.filter(name="admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_projects_dashboard(request):
    # Vista que muestra el tablero de proyectos para los admin.
    # Obtiene todos los proyectos, mensajes, publicaciones en el foro y entradas del blog.
    projects = Project.objects.all()
    messages = Message.objects.all()[:10]
    forum_posts = ForumPost.objects.select_related("topic").all()[:10]
    blog_posts = BlogPost.objects.all()[:10]

    return render(
        request,
        "projects/admin_dashboard.html",
        {
            "projects": projects,
            "messages": messages,
            "forum_posts": forum_posts,
            "blog_posts": blog_posts,
        },
    )


@login_required
def employee_projects_dashboard(request):
    # Vista del dashboard del empleado
    # Incluye proyectos asignados, tareas, documentos pendientes y cargados, y actualizaciones recientes.
    # Proyectos asignados al usuario actual
    assigned_projects = Project.objects.filter(assigned_to_employees=request.user)

    # Tareas asignadas al usuario actual
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")

    # Documentos pendientes y cargados
    pending_documents = Document.objects.filter(
        status="pending", assigned_to=request.user
    )
    uploaded_documents = Document.objects.filter(
        status="uploaded", assigned_to=request.user
    )

    # Actualizaciones recientes
    recent_updates = Update.objects.filter(project__in=assigned_projects).order_by(
        "-date"
    )[:10]

    # Cálculo del % de finalización de tareas
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="completed").count()
    task_completion_rate = (
        (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    )

    context = {
        "assigned_projects": assigned_projects,
        "tasks": tasks,
        "pending_documents": pending_documents,
        "uploaded_documents": uploaded_documents,
        "recent_updates": recent_updates,
        "task_completion_rate": task_completion_rate,
    }
    return render(request, "dashboard/employee_projects_dashboard.html", context)


@login_required
def view_projects(request):
    # Vista para ver todos los proyectos
    # el admin puede ver todos los proyectos, otros usuarios solo los asignados a ellos
    if is_admin(request.user):
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(assigned_to_employees=request.user)
    context = {
        "projects": projects,
        "is_admin": is_admin(request.user) or request.user.is_superuser,
    }
    return render(request, "projects/admin_view_projects.html", context)


@login_required
@user_passes_test(is_admin)
def create_project(request):
    # Vista para crear un nuevo proyecto
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()  # Guarda relaciones many to many
            return redirect("projects_app:view_projects")
    else:
        form = ProjectForm()
    return render(request, "projects/project_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def edit_project(request, project_id):
    # Vista para editar un proyecto existente
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects_app:view_projects")
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/project_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def update_project_status(request, project_id):
    # Vista para actualizar el estado de un proyecto
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects_app:view_project", project_id=project.id)
    else:
        form = ProjectStatusForm(instance=project)
    return render(
        request,
        "projects/update_project_status.html",
        {"form": form, "project": project},
    )


@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id):
    # Vista para eliminar un proyecto
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("projects_app:view_projects")
    return render(request, "projects/project_confirm_delete.html", {"project": project})


@login_required
def view_project(request, project_id):
    # Vista para ver detalles de un proyecto
    project = get_object_or_404(Project, pk=project_id)
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="admin").exists()
        or project.assigned_to_employees.filter(id=request.user.id).exists()
    ):
        return render(request, "projects/view_project.html", {"project": project})
    else:
        raise PermissionDenied


@login_required
def project_list(request):
    # Vista para listar proyectos según el rol del usuario
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(client=request.user)
    return render(request, "projects/project_list.html", {"projects": projects})


@login_required
@user_passes_test(is_admin)
def assignment_list(request):
    # Vista para listar asignaciones de proyectos
    assignments = ProjectAssignment.objects.all()
    return render(
        request, "projects/assignment_list.html", {"assignments": assignments}
    )


@login_required
@user_passes_test(is_admin)
def create_assignment(request):
    # Vista para crear una nueva asignación de proyecto
    # permite a los admin crear una nueva asignación de proyecto
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects_app:assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "projects/create_assignment.html", {"form": form})


# Vista de feedback
@login_required
def submit_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback")
        return HttpResponse("Thank you for your feedback!")
    else:
        return HttpResponse("Invalid request method.", status=405)


@login_required
def update_task_status(request, task_id):
    # Vista q permite a los employee actualizar el estado de una tarea/task.
    task = get_object_or_404(Task, id=task_id)
    if task.assigned_to != request.user:
        raise PermissionDenied

    if request.method == "POST":
        task.status = request.POST.get("status", task.status)
        task.save()
        return redirect("projects_app:employee_dashboard")

    return render(request, "tasks/update_task_status.html", {"task": task})


@login_required
def upload_document(request, deliverable_id):
    # Vista q permite a los usuarios cargar documentos para un entregable específico.
    # Solo el usuario asignado puede cargar documentos.
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)
    if deliverable.assigned_to != request.user:
        raise PermissionDenied

    if request.method == "POST" and "document_file" in request.FILES:
        document = Document.objects.create(
            deliverable=deliverable,
            file=request.FILES["document_file"],
            status="uploaded",
            assigned_to=request.user,
        )
        document.save()
        return redirect("projects_app:view_project", project_id=deliverable.project.id)

    return render(
        request, "documents/upload_document.html", {"deliverable": deliverable}
    )


@login_required
def create_deliverable(request, project_id):
    # Crea los entregables por proyecto
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        name = request.POST.get("name")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")
        assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
        Deliverable.objects.create(
            project=project, name=name, due_date=due_date, assigned_to=assigned_to
        )
        return redirect("projects_app:view_project", project_id=project_id)
    employees = User.objects.filter(groups__name="employee")
    return render(
        request,
        "documents/create_deliverable.html",
        {"project": project, "employees": employees},
    )


@login_required
def approve_document(request, document_id):
    # Vista q permite a los clientes aprobar documentos.
    # Con el form para cambiar el estado del documento y agregar comentarios.
    document = get_object_or_404(Document, id=document_id)
    if document.deliverable.project.client != request.user:
        raise PermissionDenied

    if request.method == "POST":
        status = request.POST.get("status")
        comments = request.POST.get("comments")
        document.status = status
        document.comments = comments
        document.save()
        return redirect(
            "projects_app:view_project", project_id=document.deliverable.project.id
        )

    return render(request, "documents/approve_document.html", {"document": document})
