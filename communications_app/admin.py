# communications_app/admin.py


from django.contrib import admin
from .models import ContactMessage, QuoteRequest


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "message", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-created_at",)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "created_at")
    list_filter = ("created_at", "service")
    search_fields = ("name", "email", "service", "message")
    ordering = ("-created_at",)
