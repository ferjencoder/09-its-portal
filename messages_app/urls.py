# messages_app/urls.py

from django.urls import path
from . import views


app_name = "messages_app"

urlpatterns = [
    path("", views.messages_view, name="messages_view"),
    path("send/<int:recipient_id>/", views.send_message, name="send_message"),
]
