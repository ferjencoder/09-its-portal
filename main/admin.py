# main/admin.py
# This file is used to register models with the Django admin site, allowing the models management through the admin interface.

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "bio", "location", "birth_date")
    list_filter = ("role", "location")
    search_fields = ("user__username", "user__email", "bio")
    ordering = ("user__username",)
