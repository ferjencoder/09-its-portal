# messages_app/models.py

from django.contrib.auth.models import User
from django.db import models


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
