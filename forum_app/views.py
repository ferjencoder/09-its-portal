# forum_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from .models import ForumPost, ForumTopic, ForumCategory
from .forms import ForumPostForm, ForumTopicForm


@login_required
def forum(request):
    # Vista para la página principal del foro
    search_query = request.GET.get("search", "")
    categories = ForumCategory.objects.all()

    if search_query:
        recent_topics = ForumTopic.objects.filter(
            title__icontains=search_query
        ).order_by("-created_at")[:10]
    else:
        recent_topics = ForumTopic.objects.order_by("-created_at")[:10]

    recent_posts = ForumPost.objects.order_by("-created_at")[:10]

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        post_data = {
            "posts": [
                {
                    "id": post.id,
                    "title": post.topic.title,
                    "content": post.content,
                    "comment_count": post.comments.count(),
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
            "recent_topics": recent_topics,
            "recent_posts": recent_posts,
            "search_query": search_query,
            "categories": categories,
        },
    )


@login_required
def topic_detail(request, topic_id):
    # Vista para los detalles de un tema específico
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
    # Vista para crear un nuevo tema en el foro
    if request.method == "POST":
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect("forum_app:topic_detail", topic_id=topic.pk)
    else:
        form = ForumTopicForm()
    categories = ForumCategory.objects.all()
    return render(
        request, "forum_app/create_topic.html", {"form": form, "categories": categories}
    )


@login_required
def create_post(request, topic_id):
    # Vista para crear una nueva publicación en un tema
    topic = get_object_or_404(ForumTopic, id=topic_id)
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                post_data = {
                    "id": post.id,
                    "title": post.topic.title,
                    "content": post.content,
                    "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "author": {
                        "profile_picture": (
                            post.author.profile.profile_picture.url
                            if post.author.profile.profile_picture
                            else None
                        ),
                    },
                    "url": reverse("forum_app:post_detail", args=[post.id]),
                    "reply_url": reverse("forum_app:create_post", args=[post.topic.id]),
                }
                return JsonResponse(post_data)
            else:
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
    # Vista para los detalles de una publicación específica
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, "forum_app/post_detail.html", {"post": post})


@login_required
def reply_post(request, post_id):
    # Vista para responder a una publicación
    post = get_object_or_404(ForumPost, id=post_id)
    posts_in_topic = ForumPost.objects.filter(topic=post.topic).order_by("-created_at")
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = post.topic
            reply.author = request.user
            reply.save()
            return redirect("forum_app:topic_detail", topic_id=post.topic.id)
    else:
        form = ForumPostForm()
    return render(
        request,
        "forum_app/reply_post.html",
        {"form": form, "post": post, "posts_in_topic": posts_in_topic},
    )
