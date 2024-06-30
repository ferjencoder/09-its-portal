# forum_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .models import ForumPost, ForumTopic
from .forms import ForumPostForm, ForumTopicForm


@login_required
def forum(request):
    topics = ForumTopic.objects.all()
    post_list = ForumPost.objects.all().order_by("-created_at")
    recent_topics = ForumTopic.objects.order_by("-created_at")[:10]
    recent_posts = ForumPost.objects.order_by("-created_at")[:10]

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        post_data = {
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "comment_count": post.comments.count(),
                    "like_count": post.like_count,
                    "view_count": post.view_count,
                    "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "profile_picture": (
                        post.author.profile.profile_picture.url
                        if post.author.profile.profile_picture
                        else None
                    ),
                    "url": reverse("forum_app:post_detail", args=[post.id]),
                    "reply_url": reverse("forum_app:create_post", args=[post.topic.id]),
                }
                for post in recent_posts
            ]
        }
        return JsonResponse(post_data)

    return render(
        request,
        "forum_app/forum.html",
        {
            "topics": topics,
            "recent_topics": recent_topics,
            "recent_posts": recent_posts,
        },
    )


@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    posts = ForumPost.objects.filter(topic=topic).order_by("-created_at")
    form = ForumPostForm()
    return render(
        request,
        "forum_app/topic_detail.html",
        {"topic": topic, "posts": posts, "form": form},
    )


@login_required
def create_topic(request):
    if request.method == "POST":
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect("forum_app:forum")
    else:
        form = ForumTopicForm()
    return render(request, "forum_app/create_topic.html", {"form": form})


@login_required
def create_post(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect("forum_app:topic_detail", topic_id=topic.id)
    else:
        form = ForumPostForm()
    topic_posts = ForumPost.objects.filter(topic=topic).order_by("-created_at")
    return render(
        request,
        "forum_app/create_post.html",
        {"form": form, "topic_posts": topic_posts, "topic": topic},
    )


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, "forum_app/post_detail.html", {"post": post})
