# forum_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ForumPost, ForumTopic
from .forms import ForumPostForm, ForumTopicForm


@login_required
def forum(request):
    topics = ForumTopic.objects.all()
    return render(request, "forum_app/forum.html", {"topics": topics})


@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    posts = ForumPost.objects.filter(topic=topic)
    return render(
        request, "forum_app/topic_detail.html", {"topic": topic, "posts": posts}
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
    return render(request, "forum_app/create_post.html", {"form": form, "topic": topic})
