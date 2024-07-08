# blog/admin.py

from django.contrib import admin
from .models import BlogPost, BlogCategory


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "body", "author__username")


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory)
