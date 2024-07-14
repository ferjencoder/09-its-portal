# communications_app/urls.py

from django.urls import path
from . import views

app_name = "communications_app"

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("request_quote/", views.request_quote, name="request_quote"),
    path(
        "request_quote/success/",
        views.request_quote_success,
        name="request_quote_success",
    ),
    path("inbox/", views.admin_inbox, name="admin_inbox"),
    path("reply/<int:message_id>/", views.reply_message, name="reply_message"),
    path("archive/<int:message_id>/", views.archive_message, name="archive_message"),
    path("archived/", views.archived_messages, name="archived_messages"),
]
