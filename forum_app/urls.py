# forum_app/urls.py

from django.urls import path
from . import views

app_name = "forum_app"

urlpatterns = [
    path("", views.forum, name="forum"),
    path("topic/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("create_topic/", views.create_topic, name="create_topic"),
    path("create_post/<int:topic_id>/", views.create_post, name="create_post"),
]
