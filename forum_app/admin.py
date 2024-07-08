# forum_app/admin.py

from django.contrib import admin
from .models import ForumPost, ForumTopic, ForumCategory

admin.site.register(ForumPost)
admin.site.register(ForumTopic)
admin.site.register(ForumCategory)
