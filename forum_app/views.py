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
    # Obtener el término de búsqueda, si existe
    search_query = request.GET.get("search", "")

    # Filtrar los temas recientes basados en el término de búsqueda
    if search_query:
        recent_topics = ForumTopic.objects.filter(
            title__icontains=search_query
        ).order_by("-created_at")[:10]
    else:
        recent_topics = ForumTopic.objects.order_by("-created_at")[:10]

    # Obtener todos los posts recientes
    recent_posts = ForumPost.objects.order_by("-created_at")[:10]

    # Comprobar si la solicitud es AJAX para cargar posts recientes
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

    # Renderizar la vista del foro
    return render(
        request,
        "forum_app/forum.html",
        {
            "recent_topics": recent_topics,
            "recent_posts": recent_posts,
            "search_query": search_query,
        },
    )


@login_required
def topic_detail(request, topic_id):
    # Obtener detalles del tema y sus posts
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
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
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
    # Obtener detalles del post
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, "forum_app/post_detail.html", {"post": post})


@login_required
def reply_post(request, post_id):
    # Responder a un post
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
