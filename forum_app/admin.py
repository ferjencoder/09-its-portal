# forum_app/admin.py

from django.contrib import admin
from .models import ForumPost, ForumTopic


admin.site.register(ForumPost)
admin.site.register(ForumTopic)
