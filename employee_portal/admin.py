# employee_portal/admin.py

from django.contrib import admin
from .models import ForumTopic, ForumPost, BlogPost, Message
from projects.models import Project

# admin.site.register(Profile)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
admin.site.register(BlogPost)
# admin.site.register(Project)
admin.site.register(Message)
