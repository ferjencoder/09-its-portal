# messages_app/views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from .models import Message, Conversation
from .forms import MessageForm
from main.utils import get_or_create_conversation


@login_required
def default_messages_view(request):
    # View to handle the display of the list of conversations for the logged-in user.
    # Filters and sorts conversations based on the time of the last message.
    search_query = request.GET.get("search", "")
    users = User.objects.exclude(id=request.user.id)

    if search_query:
        conversations = (
            Conversation.objects.filter(participants=request.user)
            .filter(participants__username__icontains=search_query)
            .annotate(last_message_time=Max("messages__created_at"))
            .order_by("-last_message_time")
        )
    else:
        conversations = (
            Conversation.objects.filter(participants=request.user)
            .annotate(last_message_time=Max("messages__created_at"))
            .order_by("-last_message_time")
        )

    conversation_details = []
    for conversation in conversations:
        last_message = conversation.messages.order_by("-created_at").first()
        recipient_user = conversation.participants.exclude(id=request.user.id).first()
        if recipient_user:
            profile_picture_url = static("assets/images/default_avatar.png")
            if (
                hasattr(recipient_user, "profile_main")
                and recipient_user.profile_main.profile_picture
            ):
                profile_picture_url = recipient_user.profile_main.profile_picture.url

            conversation_details.append(
                {
                    "id": recipient_user.id,
                    "name": recipient_user.username,
                    "avatar": profile_picture_url,
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
            "search_query": search_query,
        },
    )


@login_required
def messages_view(request, recipient_id=None):
    # View to display messages within a selected conversation.
    query = request.GET.get("search")
    user = request.user
    users = User.objects.exclude(id=request.user.id)
    recipient = None
    messages = []

    if recipient_id:
        recipient = get_object_or_404(User, id=recipient_id)
        conversation = get_or_create_conversation(user, recipient)
        messages = conversation.messages.order_by("created_at")

    conversations = (
        Conversation.objects.filter(participants=user)
        .annotate(last_message_time=Max("messages__created_at"))
        .order_by("-last_message_time")
    )

    conversation_details = []
    for conversation in conversations:
        last_message = conversation.messages.order_by("-created_at").first()
        recipient_user = conversation.participants.exclude(id=user.id).first()
        profile_picture_url = static("assets/images/default_avatar.png")
        if (
            hasattr(recipient_user, "profile_main")
            and recipient_user.profile_main.profile_picture
        ):
            profile_picture_url = recipient_user.profile_main.profile_picture.url

        conversation_details.append(
            {
                "id": recipient_user.id,
                "name": recipient_user.username,
                "avatar": profile_picture_url,
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
            "search_query": query,
        },
    )


@login_required
def send_message(request, recipient_id):
    # View to handle sending a new message to a recipient.
    if request.method == "POST":
        content = request.POST.get("content")
        recipient = get_object_or_404(User, id=recipient_id)
        conversation = get_or_create_conversation(request.user, recipient)
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content,
            conversation=conversation,
        )
        return redirect("messages_app:messages_view", recipient_id=recipient_id)
    return redirect("messages_app:default_messages_view")


@login_required
def reply_message(request, message_id):
    # View to handle replying to an existing message.
    original_message = get_object_or_404(Message, id=message_id)
    recipient = original_message.sender
    if request.method == "POST":
        content = request.POST.get("content")
        conversation = get_or_create_conversation(request.user, recipient)
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content,
            conversation=conversation,
        )
        return redirect("messages_app:messages_view", recipient_id=recipient.id)
    return render(
        request,
        "messages_app/reply_message.html",
        {"original_message": original_message},
    )


@login_required
def delete_message(request, message_id):
    # View to handle deleting a message.
    message = get_object_or_404(Message, id=message_id)
    recipient_id = (
        message.recipient.id if message.sender == request.user else message.sender.id
    )
    if message.sender == request.user or message.recipient == request.user:
        message.delete()
        return redirect("messages_app:messages_view", recipient_id=recipient_id)
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar este mensaje.")


@login_required
def edit_message(request, message_id):
    # View to allow editing an existing message.
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
    # View to handle searching for messages and displaying search results.
    query = request.GET.get("search")
    user = request.user
    conversations = []

    if query:
        # Filter messages containing the query
        messages = Message.objects.filter(
            Q(content__icontains=query) & (Q(sender=user) | Q(recipient=user))
        ).distinct()

        # Get IDs of users involved in the filtered messages
        user_ids = set(messages.values_list("sender_id", flat=True)) | set(
            messages.values_list("recipient_id", flat=True)
        )

        # Filter users by username containing the query
        users = User.objects.filter(
            Q(username__icontains=query) & Q(id__in=user_ids)
        ).distinct()

        # Combine messages and users to get conversations
        for other_user in users:
            last_message = (
                Message.objects.filter(
                    Q(sender=user, recipient=other_user)
                    | Q(sender=other_user, recipient=user)
                )
                .order_by("-created_at")
                .first()
            )

            profile_picture_url = static("assets/images/default_avatar.png")
            if (
                hasattr(other_user, "profile_main")
                and other_user.profile_main.profile_picture
            ):
                profile_picture_url = other_user.profile_main.profile_picture.url

            conversations.append(
                {
                    "id": other_user.id,
                    "name": other_user.username,
                    "avatar": profile_picture_url,
                    "last_message": last_message,
                    "last_message_time": last_message.created_at,
                }
            )

    return render(
        request,
        "messages_app/search_results.html",
        {"conversations": conversations, "search_query": query},
    )
