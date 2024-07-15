# communications_app/views.py

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from main.models import ContactMessage, QuoteRequest


def admin_inbox(request):
    contact_messages = ContactMessage.objects.filter(archived=False).order_by(
        "-created_at"
    )
    quote_requests = QuoteRequest.objects.filter(archived=False).order_by("-created_at")
    messages = list(contact_messages) + list(quote_requests)
    context = {"messages": messages}
    return render(request, "communications_app/admin_inbox.html", context)


def reply_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.read = True
    message.save()
    return JsonResponse({"status": "ok"})


def mark_as_read(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.read = True
    message.save()
    return JsonResponse({"status": "ok"})


@csrf_exempt
def archive_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.archived = True
    message.save()
    return JsonResponse({"status": "ok"})


def archived_messages(request):
    archived_contact_messages = ContactMessage.objects.filter(archived=True)
    archived_quote_requests = QuoteRequest.objects.filter(archived=True)
    messages = list(archived_contact_messages) + list(archived_quote_requests)
    context = {
        "messages": messages,
    }
    return render(request, "communications_app/archived_messages.html", context)
