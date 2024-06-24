# messages_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User


@login_required
def messages_view(request):
    messages_received = Message.objects.filter(recipient=request.user)
    messages_sent = Message.objects.filter(sender=request.user)
    return render(
        request,
        "messages_app/messages.html",
        {"messages_received": messages_received, "messages_sent": messages_sent},
    )


@login_required
def send_message(request):
    if request.method == "POST":
        recipient_id = request.POST.get("recipient")
        content = request.POST.get("content")
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(
            sender=request.user, recipient=recipient, content=content
        )
        return redirect("messages_app:messages_view")
    users = User.objects.exclude(id=request.user.id)
    return render(request, "messages_app/send_message.html", {"users": users})
