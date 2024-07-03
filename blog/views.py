# blog/views.py

import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from .models import BlogPost
from .forms import BlogPostForm


def is_admin(user):
    return user.groups.filter(name="admin").exists()


def blog_list(request):
    blog_posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/blog_list.html", {"blog_posts": blog_posts})


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog/blog_detail.html", {"post": post})


@login_required
def employee_blog_list(request):
    blog_posts = BlogPost.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "blog/employee_blog.html", {"blog_posts": blog_posts})


@login_required
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect("blog:employee_blog_list")
    else:
        form = BlogPostForm()
    return render(request, "blog/create_blog_post.html", {"form": form})


@login_required
@user_passes_test(is_admin, login_url="main:login")
def admin_blog_list(request):
    blog_posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/admin_blog.html", {"blog_posts": blog_posts})


@login_required
def edit_blog_post(request, id):
    blog_post = get_object_or_404(BlogPost, id=id)
    if blog_post.author != request.user and not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            if is_admin(request.user):
                return redirect("blog:admin_blog_list")
            return redirect("blog:employee_blog_list")
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, "blog/edit_blog_post.html", {"form": form})


@login_required
def delete_blog_post(request, id):
    blog_post = get_object_or_404(BlogPost, id=id)
    if blog_post.author != request.user and not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":
        blog_post.delete()
        if is_admin(request.user):
            return redirect("blog:admin_blog_list")
        return redirect("blog:employee_blog_list")
    return render(request, "blog/delete_blog_post.html", {"blog_post": blog_post})


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        file_path = os.path.join("blog_images", uploaded_file.name)
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        file_url = default_storage.url(saved_path)
        print(f"File uploaded successfully: {file_url}")
        return JsonResponse({"url": file_url})
    print("Upload failed")
    return JsonResponse({"error": {"message": "Upload failed"}})
