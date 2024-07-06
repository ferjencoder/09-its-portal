# Messages_app/admin.py

from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "recipient", "content", "created_at")
    search_fields = ("sender__username", "recipient__username", "content")
    list_filter = ("created_at",)


# admin.site.register(Message, MessageAdmin)
