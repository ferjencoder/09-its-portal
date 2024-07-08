# forum_app/models.py

from django.db import models
from django.contrib.auth.models import User


class ForumCategory(models.Model):
    # Model para categorías del foro
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Forum Categories"  # Corrección del nombre plural


class ForumTopic(models.Model):
    # Model para temas del foro
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        ForumCategory, related_name="topics", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="forum_topics"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    # Model para publicaciones del foro
    topic = models.ForeignKey(
        ForumTopic, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="forum_posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.topic.title}"


class ForumComment(models.Model):
    # Model para comentarios de las publicaciones del foro
    post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="forum_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.topic.title}"
