# projects_app/views.py

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main.utils import is_admin
from blog_app.models import BlogPost
from forum_app.models import ForumPost
from messages_app.models import Message
from main.models import Profile
from .models import Project, ProjectAssignment, Task, Document, Update, Deliverable
from .forms import (
    ProjectForm,
    ProjectStatusForm,
    AssignmentForm,
    DeliverableForm,
    UpdateForm,
    TaskForm,
    DocumentForm,
)


# Vista que muestra el tablero de proyectos para los administradores
@login_required
@user_passes_test(is_admin)
def admin_projects_dashboard(request):
    assigned_projects = Project.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all().select_related("project").order_by("due_date")
    pending_documents = Document.objects.filter(status="pending")
    uploaded_documents = Document.objects.filter(status="uploaded")
    recent_updates = Update.objects.all().order_by("-date")[:10]
    task_completion_rate = (
        tasks.filter(status="completed").count() / tasks.count() * 100
        if tasks.count() > 0
        else 0
    )
    project_form = ProjectForm()
    update_form = UpdateForm()
    task_form = TaskForm()
    document_form = DocumentForm()

    context = {
        "projects": projects,
        "assigned_projects": assigned_projects,
        "tasks": tasks,
        "pending_documents": pending_documents,
        "uploaded_documents": uploaded_documents,
        "recent_updates": recent_updates,
        "task_completion_rate": task_completion_rate,
        "project_form": project_form,
        "update_form": update_form,
        "task_form": task_form,
        "document_form": document_form,
    }
    return render(request, "dashboard/admin_projects_dashboard.html", context)


# Vista que muestra el tablero de proyectos para los empleados
@login_required
def employee_projects_dashboard(request):
    assigned_projects = Project.objects.filter(assigned_to_employees=request.user)
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    pending_documents = Document.objects.filter(
        status="pending", project__in=assigned_projects
    )
    uploaded_documents = Document.objects.filter(
        status="uploaded", project__in=assigned_projects
    )
    recent_updates = Update.objects.filter(project__in=assigned_projects).order_by(
        "-date"
    )[:10]
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="completed").count()
    task_completion_rate = (
        (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    )

    project_form = ProjectForm()
    task_form = TaskForm()
    update_form = UpdateForm()
    document_form = DocumentForm()

    context = {
        "assigned_projects": assigned_projects,
        "tasks": tasks,
        "pending_documents": pending_documents,
        "uploaded_documents": uploaded_documents,
        "recent_updates": recent_updates,
        "task_completion_rate": task_completion_rate,
        "project_form": project_form,
        "task_form": task_form,
        "update_form": update_form,
        "document_form": document_form,
    }
    return render(request, "dashboard/employee_projects_dashboard.html", context)


# Vista del tablero del cliente
@login_required
def client_projects_dashboard(request):
    client_projects = Project.objects.filter(assigned_to_client=request.user)
    tasks = Task.objects.filter(project__in=client_projects).order_by("due_date")
    pending_documents = Document.objects.filter(
        project__in=client_projects, status="pending"
    )
    uploaded_documents = Document.objects.filter(
        project__in=client_projects, status="uploaded"
    )
    recent_updates = Update.objects.filter(project__in=client_projects).order_by(
        "-date"
    )[:10]
    task_completion_rate = (
        tasks.filter(status="completed").count() / tasks.count() * 100
        if tasks.count() > 0
        else 0
    )

    project_form = ProjectForm()
    update_form = UpdateForm()
    task_form = TaskForm()
    document_form = DocumentForm()

    messages = Message.objects.filter(recipient=request.user)[:10]
    forum_posts = ForumPost.objects.filter(author=request.user).select_related("topic")[
        :10
    ]
    blog_posts = BlogPost.objects.filter(author=request.user)[:10]

    context = {
        "client_projects": client_projects,
        "tasks": tasks,
        "pending_documents": pending_documents,
        "uploaded_documents": uploaded_documents,
        "recent_updates": recent_updates,
        "task_completion_rate": task_completion_rate,
        "project_form": project_form,
        "update_form": update_form,
        "task_form": task_form,
        "document_form": document_form,
        "messages": messages,
        "forum_posts": forum_posts,
        "blog_posts": blog_posts,
        "projects": client_projects,
    }
    return render(request, "dashboard/client_projects_dashboard.html", context)


# Vista para ver todos los proyectos
@login_required
def view_projects(request):
    if is_admin(request.user):
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(assigned_to_employees=request.user)
    context = {
        "projects": projects,
        "is_admin": is_admin(request.user) or request.user.is_superuser,
    }
    return render(request, "projects/admin_view_projects.html", context)


# Vista para crear un nuevo proyecto
@login_required
@user_passes_test(is_admin)
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "dashboard/project_list_item.html",
                    {"project": project},
                    request=request,
                )
                return JsonResponse(
                    {"message": "Project created successfully!", "html": html}
                )
            return redirect("projects_app:admin_projects_dashboard")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = ProjectForm()

    return render(request, "projects/project_form.html", {"form": form})


# Vista para editar un proyecto existente
@login_required
@user_passes_test(is_admin)
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.assigned_to_client = form.cleaned_data["assigned_to_client"]
            project.save()
            form.save_m2m()
            return redirect("projects_app:view_projects")
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/project_form.html", {"form": form})


# Vista para actualizar el estado de un proyecto
@login_required
@user_passes_test(is_admin)
def update_project_status(request, project_id):
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


# Vista para eliminar un proyecto
@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("projects_app:admin_projects_dashboard")
    return render(request, "projects/project_confirm_delete.html", {"project": project})


# Vista para ver detalles de un proyecto
@login_required
def view_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if (
        request.user.is_superuser
        or request.user.groups.filter(name="admin").exists()
        or project.assigned_to_employees.filter(id=request.user.id).exists()
    ):
        return render(request, "projects/view_project.html", {"project": project})
    else:
        raise PermissionDenied


# Vista para listar proyectos según el rol del usuario
@login_required
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(client=request.user)
    return render(request, "projects/project_list.html", {"projects": projects})


# Vista para listar asignaciones de proyectos
@login_required
@user_passes_test(is_admin)
def assignment_list(request):
    assignments = ProjectAssignment.objects.all()
    return render(
        request, "projects/assignment_list.html", {"assignments": assignments}
    )


# Vista para crear una nueva asignación de proyecto
@login_required
@user_passes_test(is_admin)
def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects_app:assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "projects/create_assignment.html", {"form": form})


# Vista para enviar feedback
@login_required
def submit_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get("feedback")
        return HttpResponse("¡Gracias por tus comentarios!")
    else:
        return HttpResponse("Método de solicitud no válido.", status=405)


# Vista para crear tareas
@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user  # Asigna la tarea al usuario actual
            if not task.project:
                task.is_personal = True  # Marca la tarea como personal si no tiene un proyecto asignado
            task.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"message": "Task created successfully!"})

            # Determina el rol del usuario y redirige en consecuencia
            profile = Profile.objects.get(user=request.user)
            if profile.role == "admin":
                return redirect("projects_app:admin_projects_dashboard")
            elif profile.role == "employee":
                return redirect("projects_app:employee_projects_dashboard")
            elif profile.role == "client":
                return redirect("projects_app:client_projects_dashboard")
            else:
                return redirect("main:dashboard")
        else:
            print(form.errors)
    else:
        form = TaskForm()

    # Proporciona la variable 'projects' para el formulario
    profile = Profile.objects.get(user=request.user)
    if profile.role == "employee":
        projects = Project.objects.filter(assigned_to_employees=request.user)
    elif profile.role == "client":
        projects = Project.objects.filter(assigned_to_client=request.user)
    else:
        projects = Project.objects.all()

    return render(
        request, "tasks/create_task.html", {"form": form, "projects": projects}
    )


# Vista para editar una tarea existente
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            profile = Profile.objects.get(user=request.user)
            if profile.role == "admin":
                return redirect("projects_app:admin_projects_dashboard")
            elif profile.role == "employee":
                return redirect("projects_app:employee_projects_dashboard")
            elif profile.role == "client":
                return redirect("projects_app:client_projects_dashboard")
            else:
                return redirect("main:dashboard")
    else:
        form = TaskForm(instance=task)

    projects = Project.objects.all()
    return render(
        request,
        "tasks/edit_task.html",
        {"form": form, "task": task, "projects": projects},
    )


# Vista para eliminar una tarea existente
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        profile = Profile.objects.get(user=request.user)
        if profile.role == "admin":
            return redirect("projects_app:admin_projects_dashboard")
        elif profile.role == "employee":
            return redirect("projects_app:employee_projects_dashboard")
        elif profile.role == "client":
            return redirect("projects_app:client_projects_dashboard")
        else:
            return redirect("main:dashboard")
    return render(request, "tasks/confirm_delete_task.html", {"task": task})


# Vista que permite a los empleados actualizar el estado de una tarea
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user

    # Verificar si el usuario es un administrador
    if is_admin(user):
        # Los administradores pueden actualizar el estado de cualquier tarea
        if request.method == "POST":
            task.status = request.POST.get("status", task.status)
            task.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {"message": "¡Estado de la tarea actualizado exitosamente!"}
                )
            return redirect("projects_app:admin_projects_dashboard")
    else:
        # Verificar si la tarea está asignada al usuario actual o si el usuario forma parte de los empleados o clientes del proyecto
        if (
            task.assigned_to == user
            or task.project.assigned_to_employees.filter(id=user.id).exists()
            or task.project.assigned_to_client == user
        ):
            if request.method == "POST":
                task.status = request.POST.get("status", task.status)
                task.save()
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse(
                        {"message": "¡Estado de la tarea actualizado exitosamente!"}
                    )
                return redirect("projects_app:employee_projects_dashboard")
        else:
            raise PermissionDenied

    return JsonResponse({"message": "Solicitud inválida"}, status=400)


# Vista que permite a los usuarios cargar documentos para un entregable específico
@login_required
def upload_document(request, deliverable_id):
    print(f"Deliverable ID: {deliverable_id}")  # Debugging statement
    # Obtener el entregable o devolver un error 404 si no existe
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)

    print(f"Deliverable: {deliverable}")  # Debugging statement

    # Verificar que el usuario asignado al entregable es el mismo que está haciendo la solicitud
    if deliverable.assigned_to != request.user:
        raise PermissionDenied

    # Si el método es POST y se proporciona un archivo en la solicitud
    if request.method == "POST" and "document_file" in request.FILES:
        # Crear un nuevo documento asociado al entregable
        document = Document.objects.create(
            project=deliverable.project,
            name=request.FILES["document_file"].name,
            file=request.FILES["document_file"],
            status="uploaded",
            assigned_to=request.user,
        )
        document.save()
        print(f"Document uploaded: {document}")  # Debugging statement
        # Redirigir a la vista del proyecto después de subir el documento
        return redirect("projects_app:view_project", project_id=deliverable.project.id)

    # Renderizar la plantilla de carga de documentos si no es una solicitud POST
    return render(
        request, "documents/upload_document.html", {"deliverable": deliverable}
    )


# Vista para crear un nuevo entregable
@login_required
def create_deliverable(request, project_id):
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


# Vista para editar un entregable
@login_required
def edit_deliverable(request, deliverable_id):
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


# Vista para eliminar un entregable
@login_required
@user_passes_test(is_admin)
def delete_deliverable(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, id=deliverable_id)
    project_id = deliverable.project.id
    if request.method == "POST":
        deliverable.delete()
        return redirect("projects_app:view_project", project_id=project_id)
    return render(
        request, "documents/delete_deliverable.html", {"deliverable": deliverable}
    )


# Vista para agregar un nuevo deliverable
@login_required
def add_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.assigned_to = request.user
            document.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "message": "Document added successfully!",
                        "document_name": document.name,
                        "document_id": document.id,
                    }
                )

            # Determina el rol del usuario y redirige en consecuencia
            profile = Profile.objects.get(user=request.user)
            if profile.role == "admin":
                return redirect("projects_app:admin_projects_dashboard")
            elif profile.role == "employee":
                return redirect("projects_app:employee_projects_dashboard")
            elif profile.role == "client":
                return redirect("projects_app:client_projects_dashboard")
            else:
                return redirect("main:dashboard")
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    else:
        form = DocumentForm()

    # Manejado via AJAX no renderizo template
    return JsonResponse({"errors": form.errors}, status=400)


# Vista para mostrar la historia del documento
def document_history(request, document_id):
    document = Document.objects.get(pk=document_id)
    revisions = document.revisions.all()
    return render(
        request, "document_history.html", {"document": document, "revisions": revisions}
    )


# Vista que permite a los clientes aprobar documentos
@login_required
def approve_document(request, document_id):
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


# Vista para crear una nueva actualización
@login_required
def create_update(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.date = timezone.now()
            update.project = form.cleaned_data["project"]
            update.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string(
                    "dashboard/update_list_item.html",
                    {"update": update, "project": update.project},
                    request=request,
                )
                return JsonResponse(
                    {"message": "Update created successfully!", "html": html}
                )

            # Determina el rol del usuario y redirige en consecuencia
            profile = Profile.objects.get(user=request.user)
            if profile.role == "admin":
                return redirect("projects_app:admin_projects_dashboard")
            elif profile.role == "employee":
                return redirect("projects_app:employee_projects_dashboard")
            elif profile.role == "client":
                return redirect("projects_app:client_projects_dashboard")
            else:
                return redirect("projects_app:admin_projects_dashboard")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = UpdateForm()

    return render(request, "projects/create_update.html", {"form": form})


# Vista para obtener las recent updates
def recent_updates_view(request):
    recent_updates = (
        Update.objects.select_related("project").all().order_by("-date")[:10]
    )
    context = {
        "recent_updates": recent_updates,
    }
    return render(request, "projects_app/dashboard/recent_updates.html", context)
