# messages_app/models.py

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {', '.join(user.username for user in self.participants.all())}"

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
        db_index=True,
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages", db_index=True
    )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender} To: {self.recipient} - {self.content[:30]}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not self.content:
            raise ValueError("Content cannot be empty")

    class Meta:
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["recipient"]),
        ]
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
