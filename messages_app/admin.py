# messages_app/admin.py

from django.contrib import admin
from .models import Message, Conversation


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "content", "created_at")
    search_fields = ("sender__username", "recipient__username", "content")
    list_filter = ("created_at",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "get_participants", "created_at")
    search_fields = ("participants__username",)
    list_filter = ("created_at",)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])

    get_participants.short_description = "Participants"
