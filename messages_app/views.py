# messages_app/views.py

import json
from django.db.models import Max, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from django.templatetags.static import static


@login_required
def messages_view(request, recipient_id=None):
    users = User.objects.exclude(id=request.user.id)
    recipient = None
    messages = []

    if recipient_id:
        recipient = get_object_or_404(User, id=recipient_id)
        messages = Message.objects.filter(
            Q(sender=request.user, recipient=recipient)
            | Q(sender=recipient, recipient=request.user)
        ).order_by("created_at")

    conversations = (
        Message.objects.filter(sender=request.user)
        .values("recipient")
        .annotate(last_message_time=Max("created_at"))
        .union(
            Message.objects.filter(recipient=request.user)
            .values("sender")
            .annotate(last_message_time=Max("created_at"))
        )
        .order_by("-last_message_time")
    )

    conversation_details = []
    for convo in conversations:
        last_message = (
            Message.objects.filter(
                Q(sender=request.user, recipient_id=convo["recipient"])
                | Q(recipient=request.user, sender_id=convo["recipient"])
            )
            .order_by("-created_at")
            .first()
        )

        recipient_user = User.objects.get(id=convo["recipient"])
        conversation_details.append(
            {
                "id": recipient_user.id,
                "name": recipient_user.username,
                "avatar": (
                    recipient_user.profile.profile_picture.url
                    if recipient_user.profile.profile_picture
                    else static("assets/images/default_avatar.png")
                ),
                "last_message": last_message,
                "last_message_time": last_message.created_at,
            }
        )

    return render(
        request,
        "messages_app/messages.html",
        {
            "messages": messages,
            "users": users,
            "conversations": conversation_details,
            "recipient": recipient,
        },
    )


@login_required
def send_message(request, recipient_id):
    if request.method == "POST":
        content = request.POST.get("content")
        recipient = get_object_or_404(User, id=recipient_id)
        Message.objects.create(
            sender=request.user, recipient=recipient, content=content
        )
        return redirect("messages_app:messages_view", recipient_id=recipient_id)
    return redirect("messages_app:messages_view")
