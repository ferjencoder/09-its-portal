# projects_app/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import BlogPost
from forum_app.models import ForumPost
from messages_app.models import Message
from .models import Project, ProjectAssignment, Task, Document, Update, Deliverable
from .forms import ProjectForm, ProjectStatusForm, AssignmentForm, DeliverableForm


def is_admin(user):
    # Verifica si el usuario es admin
    return user.groups.filter(name="admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_projects_dashboard(request):
    # Vista que muestra el tablero de proyectos para los admin.
    projects = Project.objects.all()
    messages = Message.objects.all()[:10]
    forum_posts = ForumPost.objects.select_related("topic").all()[:10]
    blog_posts = BlogPost.objects.all()[:10]

    return render(
        request,
        "dashboard/admin_projects_dashboard.html",
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
    assigned_projects = Project.objects.filter(assigned_to_employees=request.user)
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    pending_documents = Document.objects.filter(
        status="pending", assigned_to=request.user
    )
    uploaded_documents = Document.objects.filter(
        status="uploaded", assigned_to=request.user
    )
    recent_updates = Update.objects.filter(project__in=assigned_projects).order_by(
        "-date"
    )[:10]
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
            form.save_m2m()
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
        return HttpResponse("¡Gracias por tus comentarios!")
    else:
        return HttpResponse("Método de solicitud no válido.", status=405)


@login_required
def update_task_status(request, task_id):
    # Vista que permite a los empleados actualizar el estado de una tarea.
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
    # Vista que permite a los usuarios cargar documentos para un entregable específico.
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
    else:
        return HttpResponse("No se proporcionó el archivo del documento.", status=400)

    return render(
        request, "documents/upload_document.html", {"deliverable": deliverable}
    )


@login_required
def create_deliverable(request, project_id):
    # Vista para crear un nuevo entregable
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        name = request.POST.get("name")
        due_date = request.POST.get("due_date")
        status = request.POST.get("status")
        assigned_to_id = request.POST.get("assigned_to")
        assigned_to = User.objects.get(id=assigned_to_id) if assigned_to_id else None
        Deliverable.objects.create(
            project=project,
            name=name,
            due_date=due_date,
            status=status,
            assigned_to=assigned_to,
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
    # Vista que permite a los clientes aprobar documentos.
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


@login_required
@user_passes_test(is_admin)
def delete_deliverable(request, deliverable_id):
    # Vista para eliminar un entregable
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)
    project_id = deliverable.project.id
    if request.method == "POST":
        deliverable.delete()
        return redirect("projects_app:view_project", project_id=project_id)
    return render(
        request, "documents/delete_deliverable.html", {"deliverable": deliverable}
    )


@login_required
def edit_deliverable(request, deliverable_id):
    # Vista para editar un entregable
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)
    if request.method == "POST":
        form = DeliverableForm(request.POST, instance=deliverable)
        if form.is_valid():
            form.save()
            return redirect(
                "projects_app:view_project", project_id=deliverable.project.id
            )
    else:
        form = DeliverableForm(instance=deliverable)
    return render(
        request,
        "documents/edit_deliverable.html",
        {"form": form, "deliverable": deliverable},
    )
