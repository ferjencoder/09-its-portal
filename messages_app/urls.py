# messages_app/urls.py

from django.urls import path
from . import views

app_name = "messages_app"

urlpatterns = [
    path("", views.default_messages_view, name="default_messages_view"),
    path("conversation/<int:recipient_id>/", views.messages_view, name="messages_view"),
    path("send/<int:recipient_id>/", views.send_message, name="send_message"),
    path("reply_message/<int:message_id>/", views.reply_message, name="reply_message"),
    path("delete/<int:message_id>/", views.delete_message, name="delete_message"),
]
