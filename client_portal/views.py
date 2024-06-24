# client_portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from main.models import Profile
from blog.models import BlogPost
from messages_app.models import Message
from forum_app.models import ForumPost
from .forms import ProfileForm


@login_required
def client_dashboard(request):
    projects = Project.objects.filter(client=request.user)
    messages = Message.objects.filter(recipient=request.user)
    forum_posts = ForumPost.objects.all()
    blog_posts = BlogPost.objects.all()
    return render(
        request,
        "client_portal/client_dashboard.html",
        {
            "projects": projects,
            "messages": messages,
            "forum_posts": forum_posts,
            "blog_posts": blog_posts,
        },
    )


@login_required
def view_projects(request):
    projects = Project.objects.filter(client=request.user)
    return render(request, "client_portal/view_projects.html", {"projects": projects})


@login_required
def profile(request):
    return render(request, "client_portal/profile.html")


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("client_portal:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "client_portal/edit_profile.html", {"form": form})


@login_required
def project_list(request):
    projects = Project.objects.filter(client=request.user)
    return render(request, "client_portal/project_list.html", {"projects": projects})


@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, "client_portal/project_detail.html", {"project": project})
