# projects_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Project, ProjectAssignment
from .forms import ProjectForm, ProjectStatusForm, AssignmentForm
from messages_app.models import Message
from forum_app.models import ForumPost
from blog_app.models import BlogPost


# Verifica si el usuario es administrador
def is_admin(user):
    return user.groups.filter(name="admin").exists()


# Vista del dashboard del administrador
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
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


# Vista para ver todos los proyectos
@login_required
@user_passes_test(is_admin)
def view_projects(request):
    projects = Project.objects.all()
    return render(request, "projects/view_projects.html", {"projects": projects})


# Vista para crear un nuevo proyecto
@login_required
@user_passes_test(is_admin)
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects_app:view_projects")
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
            form.save()
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
        return redirect("projects_app:project_list")
    return render(request, "projects/project_confirm_delete.html", {"project": project})


# Vista para ver detalles de un proyecto
@login_required
def view_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if (
        request.user.is_superuser
        or project.client == request.user
        or project.assigned_to == request.user
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
