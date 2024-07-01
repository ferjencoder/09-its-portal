# projects/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Project
from .forms import ProjectForm, ProjectStatusForm
from blog.models import BlogPost
from django.views.generic import DeleteView


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_blog_list(request):
    blog_posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/admin_blog_list.html", {"blog_posts": blog_posts})


@login_required
def project_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(client=request.user)
    return render(request, "projects/project_list.html", {"projects": projects})


@login_required
@user_passes_test(is_admin)
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect("projects:view_project", project_id=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/project_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def update_project_status(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:view_project", project_id=project.id)
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
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("projects:project_list")
    return render(request, "projects/project_confirm_delete.html", {"project": project})


@login_required
def view_projects(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(client=request.user)
    return render(request, "projects/view_projects.html", {"projects": projects})


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
