# main/admin.py
# This file is used to register models with the Django admin site, allowing the models management through the admin interface.

from django.contrib import admin
from .models import Profile, ContactMessage, QuoteRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "bio", "location", "birth_date")
    list_filter = ("role", "location")
    search_fields = ("user__username", "user__email", "bio")
    ordering = ("user__username",)


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
