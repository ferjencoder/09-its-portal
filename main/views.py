# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import Profile
from .utils import get_profile
from django.utils import translation
from forum_app.models import ForumTopic
from messages_app.models import Message
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect


def csrf_failure(request, reason=""):
    return HttpResponse("CSRF verification failed. Reason: %s" % reason)


def set_language(request):
    user_language = request.GET.get("language", "en")
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect(request.META.get("HTTP_REFERER"))


def home(request):
    return render(request, "main/home.html")


def about(request):
    return render(request, "main/about.html")


def contact(request):
    return render(request, "main/contact.html")


def services(request):
    return render(request, "main/services.html")


def request_quote(request):
    return render(request, "main/request_quote.html")


@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")
            if role == "client":
                group = Group.objects.get(name="client")
            elif role == "employee":
                group = Group.objects.get(name="employee")
            elif role == "admin":
                group = Group.objects.get(name="admin")
            else:
                group = Group.objects.get(name="user")
            user.groups.add(group)
            login(request, user)
            return redirect("main:home")
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {"form": form})


@login_required
def messages_view(request):
    messages = Message.objects.filter(recipient=request.user)
    return render(request, "messages_app/messages.html", {"messages": messages})


@login_required
def profile(request):
    profile = get_profile(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("main:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "main/profile.html", {"form": form})


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    if profile:
        if profile.role == "employee":
            topics = ForumTopic.objects.all()
            messages_list = Message.objects.filter(recipient=request.user)
            return render(
                request,
                "employee_portal/employee_dashboard.html",
                {"profile": profile, "topics": topics, "messages": messages_list},
            )
        elif profile.role == "client":
            return render(request, "client_portal/client_dashboard.html")
        elif profile.role == "admin":
            return render(request, "its_admin/admin_dashboard.html")
        else:
            return render(request, "main/user_dashboard.html")
    else:
        return redirect("main:create_profile")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:home")
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main:home")
