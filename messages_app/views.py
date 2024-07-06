# messages_app/views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from .models import Message
from .forms import MessageForm


@login_required
def default_messages_view(request):
    users = User.objects.exclude(id=request.user.id)
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values("recipient", "sender")
        .annotate(last_message_time=Max("created_at"))
        .order_by("-last_message_time")
    )

    conversation_details = []
    for convo in conversations:
        other_user_id = (
            convo["recipient"]
            if convo["sender"] == request.user.id
            else convo["sender"]
        )
        last_message = (
            Message.objects.filter(
                Q(sender=request.user, recipient_id=other_user_id)
                | Q(recipient=request.user, sender_id=other_user_id)
            )
            .order_by("-created_at")
            .first()
        )
        recipient_user = User.objects.get(id=other_user_id)
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
            "users": users,
            "conversations": conversation_details,
        },
    )


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
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values("recipient", "sender")
        .annotate(last_message_time=Max("created_at"))
        .order_by("-last_message_time")
    )

    conversation_details = []
    for convo in conversations:
        other_user_id = (
            convo["recipient"]
            if convo["sender"] == request.user.id
            else convo["sender"]
        )
        last_message = (
            Message.objects.filter(
                Q(sender=request.user, recipient_id=other_user_id)
                | Q(recipient=request.user, sender_id=other_user_id)
            )
            .order_by("-created_at")
            .first()
        )
        recipient_user = User.objects.get(id=other_user_id)
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
    return redirect("messages_app:default_messages_view")


@login_required
def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    recipient = original_message.sender
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(
            sender=request.user, recipient=recipient, content=content
        )
        return redirect("messages_app:messages_view", recipient_id=recipient.id)
    return render(
        request,
        "messages_app/reply_message.html",
        {"original_message": original_message},
    )


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    recipient_id = (
        message.recipient.id if message.sender == request.user else message.sender.id
    )
    if message.sender == request.user or message.recipient == request.user:
        message.delete()
        return redirect("messages_app:messages_view", recipient_id=recipient_id)
    else:
        return HttpResponseForbidden("You are not allowed to delete this message.")


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect(
                "messages_app:messages_view", recipient_id=message.recipient.id
            )
    else:
        form = MessageForm(instance=message)
    return render(
        request, "messages_app/edit_message.html", {"form": form, "message": message}
    )


@login_required
def search_messages(request):
    query = request.GET.get("q")
    if query:
        messages = Message.objects.filter(
            Q(content__icontains=query)
            & (Q(sender=request.user) | Q(recipient=request.user))
        ).order_by("-created_at")
    else:
        messages = Message.objects.none()

    return render(request, "messages_app/search_results.html", {"messages": messages})
