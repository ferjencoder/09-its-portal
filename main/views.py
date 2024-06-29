# main/views.py

from django.conf import settings
from django.core.files import File
from django.utils import translation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm, ProfileForm, UserRegistrationForm, UserEditForm
from .models import Profile
from .utils import get_profile
from forum_app.models import ForumTopic
from messages_app.models import Message
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import os
import shutil
import logging

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    return HttpResponse("CSRF verification failed. Reason: %s" % reason)


@login_required
def some_view(request):
    user_role = request.user.groups.first().name
    if user_role == "admin":
        return render(request, "main/sidebar_admin.html")
    elif user_role == "employee":
        return render(request, "main/sidebar_employee.html")
    elif user_role == "client":
        return render(request, "main/sidebar_client.html")
    else:
        return render(request, "main/sidebar_generic.html")


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
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")
            if role == "client":
                group = Group.objects.get(name="client")
            elif role == "employee":
                group = Group.objects.get(name="employee")
            elif role == "admin":
                group = Group.objects.get(name="admin")
            user.save()
            user.groups.add(group)
            profile, created = Profile.objects.get_or_create(
                user=user, defaults={"role": role}
            )
            if not created:
                profile.role = role
                profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
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
def edit_profile(request):
    profile = get_profile(request.user)

    predefined_images = [
        f"assets/images/avatars/{image}"
        for image in os.listdir(
            os.path.join(settings.BASE_DIR, "its_portal/static/assets/images/avatars")
        )
    ]

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        predefined_image = request.POST.get("predefined_image")
        current_password = request.POST.get("current_password")
        confirm_current_password = request.POST.get("confirm_current_password")

        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"Predefined image: {predefined_image}")

        if current_password != confirm_current_password:
            messages.error(request, "Current passwords do not match.")
        elif not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()

                profile = profile_form.save(commit=False)

                if predefined_image:
                    predefined_image_path = os.path.join(
                        settings.BASE_DIR,
                        "its_portal/static/assets/images/avatars",
                        os.path.basename(predefined_image),
                    )
                    media_path = os.path.join(
                        settings.MEDIA_ROOT,
                        "profile_images",
                        os.path.basename(predefined_image),
                    )
                    os.makedirs(
                        os.path.dirname(media_path), exist_ok=True
                    )  # Ensure the directory exists
                    if os.path.exists(predefined_image_path):
                        try:
                            shutil.copy(predefined_image_path, media_path)
                            profile.profile_picture = os.path.join(
                                "profile_images", os.path.basename(predefined_image)
                            )
                            logger.debug(
                                f"Profile picture set to: {profile.profile_picture}"
                            )
                        except FileNotFoundError as e:
                            logger.error(f"Error copying predefined image: {e}")
                            messages.error(
                                request, f"Error copying predefined image: {e}"
                            )
                    else:
                        logger.error(
                            f"Predefined image not found: {predefined_image_path}"
                        )
                        messages.error(
                            request,
                            f"Predefined image not found: {predefined_image_path}",
                        )

                profile.save()
                messages.success(request, "Your profile has been updated!")
                return redirect("main:profile")
            else:
                logger.debug(f"Form errors: {user_form.errors}, {profile_form.errors}")
                messages.error(request, "Please correct the errors below.")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "main/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "predefined_images": predefined_images,
        },
    )


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
                form.add_error(None, "Invalid username or password")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main:home")


# TEST
def test_media_static(request):
    return render(
        request,
        "main/test_media_static.html",
        {
            "media_url": settings.MEDIA_URL,
            "static_url": settings.STATIC_URL,
        },
    )
