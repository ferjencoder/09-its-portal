from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User


@login_required
def messages_view(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, "messages_app/messages.html", {"messages": messages})


@login_required
def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(
            sender=request.user, recipient=recipient, content=content
        )
        return redirect("messages_app:messages_view")
    return render(request, "messages_app/send_message.html", {"recipient": recipient})
