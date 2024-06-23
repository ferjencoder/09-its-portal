from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm


def blog_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, "blog/blog.html", {"blog_posts": blog_posts})


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog/blog_detail.html", {"post": post})


def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("blog_list")
    else:
        form = BlogPostForm()
    return render(request, "blog/create_blog_post.html", {"form": form})
