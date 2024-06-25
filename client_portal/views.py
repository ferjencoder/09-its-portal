# client_portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from main.models import Profile
from blog.models import BlogPost
from django.contrib import messages
from messages_app.models import Message
from forum_app.models import ForumPost
from main.forms import UserRegistrationForm, ProfileForm
from main.utils import get_profile


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
    profile = get_profile(request.user)
    return render(request, "client_portal/profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    profile = get_profile(request.user)
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("client_portal:profile")
    else:
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(
        request,
        "client_portal/edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def project_list(request):
    projects = Project.objects.filter(client=request.user)
    return render(request, "client_portal/project_list.html", {"projects": projects})


@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, "client_portal/project_detail.html", {"project": project})
