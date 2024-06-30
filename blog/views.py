# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required


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
