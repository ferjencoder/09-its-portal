# communications_app/views.py


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import ContactMessage, QuoteRequest


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import ContactMessage, QuoteRequest
from .forms import ContactForm, QuoteRequestForm


def contact(request):
    show_success_modal = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("communications_app:contact_success")
    else:
        form = ContactForm()
    return render(request, "communications_app/contact.html", {"form": form})


def contact_success(request):
    return render(
        request, "communications_app/contact.html", {"show_success_modal": True}
    )


def request_quote(request):
    show_success_modal = False
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your quote request has been sent successfully!")
            return redirect("communications_app:request_quote")
    else:
        form = QuoteRequestForm()
    return render(
        request,
        "communications_app/request_quote.html",
        {"form": form, "show_success_modal": show_success_modal},
    )


def request_quote_success(request):
    return render(
        request,
        "communications_app/request_quote_success.html",
        {"show_success_modal": True},
    )


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


def archive_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.archived = True
    message.save()
    return JsonResponse({"status": "ok"})


def archived_messages(request):
    contact_messages = ContactMessage.objects.filter(archived=True).order_by(
        "-created_at"
    )
    quote_requests = QuoteRequest.objects.filter(archived=True).order_by("-created_at")
    messages = list(contact_messages) + list(quote_requests)
    context = {"messages": messages}
    return render(request, "communications_app/archived_messages.html", context)
