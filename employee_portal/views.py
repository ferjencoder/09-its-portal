# employee_portal/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from main.models import Profile
from messages_app.models import Message
from forum_app.models import ForumPost
from blog.models import BlogPost
from .forms import BlogPostForm, ProfileForm


@login_required
def employee_dashboard(request):
    projects = Project.objects.filter(assigned_to=request.user)
    messages = Message.objects.filter(recipient=request.user)
    forum_posts = ForumPost.objects.all()
    blog_posts = BlogPost.objects.all()
    return render(
        request,
        "employee_portal/employee_dashboard.html",
        {
            "projects": projects,
            "messages": messages,
            "forum_posts": forum_posts,
            "blog_posts": blog_posts,
        },
    )


@login_required
def documents(request):
    return render(request, "employee_portal/documents.html")


@login_required
def approve_work(request):
    return render(request, "employee_portal/approve_work.html")


@login_required
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect("employee_portal:employee_dashboard")
    else:
        form = BlogPostForm()
    return render(request, "employee_portal/create_blog_post.html", {"form": form})


@login_required
def profile(request):
    return render(request, "employee_portal/profile.html")


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("employee_portal:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "employee_portal/edit_profile.html", {"form": form})
