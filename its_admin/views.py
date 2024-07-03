# its_admin/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project
from messages_app.models import Message
from forum_app.models import ForumPost, ForumTopic
from blog.models import BlogPost
from .forms import ProjectForm


def is_admin(user):
    return user.groups.filter(name="admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    projects = Project.objects.all()
    messages = Message.objects.all()[:10]  # Fetch the latest 10 messages
    forum_posts = ForumPost.objects.select_related("topic").all()[
        :10
    ]  # Fetch the latest 10 forum posts
    blog_posts = BlogPost.objects.all()[:10]  # Fetch the latest 10 blog posts

    return render(
        request,
        "its_admin/admin_dashboard.html",
        {
            "projects": projects,
            "messages": messages,
            "forum_posts": forum_posts,
            "blog_posts": blog_posts,
        },
    )


@login_required
@user_passes_test(is_admin)
def view_projects(request):
    projects = Project.objects.all()
    return render(request, "its_admin/view_projects.html", {"projects": projects})


@login_required
@user_passes_test(is_admin)
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("its_admin:view_projects")
    else:
        form = ProjectForm()
    return render(request, "its_admin/project_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("its_admin:view_projects")
    else:
        form = ProjectForm(instance=project)
    return render(request, "its_admin/project_form.html", {"form": form})
