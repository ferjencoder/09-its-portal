# its_admin/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assignment, Project
from .forms import AssignmentForm, ProjectForm


def is_admin(user):
    return user.groups.filter(name="admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    assignments = Assignment.objects.all()
    projects = Project.objects.all()
    return render(
        request,
        "its_admin/admin_dashboard.html",
        {
            "assignments": assignments,
            "projects": projects,
        },
    )


@login_required
@user_passes_test(is_admin)
def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("its_admin:admin_dashboard")
    else:
        form = AssignmentForm()
    return render(request, "its_admin/create_assignment.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user  # Set the client to the current user
            project.save()
            return redirect("its_admin:admin_dashboard")
    else:
        form = ProjectForm()
    return render(request, "its_admin/create_project.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(
        request, "its_admin/assignment_list.html", {"assignments": assignments}
    )


@login_required
@user_passes_test(is_admin)
def project_list(request):
    projects = Project.objects.all()
    return render(request, "its_admin/project_list.html", {"projects": projects})
