# main/views.py

import os
import shutil
import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import translation
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, ProfileForm, UserEditForm
from .models import Profile
from .utils import get_profile
from forum_app.models import ForumTopic, ForumPost
from messages_app.models import Message
from projects_app.models import Project
from blog_app.models import BlogPost

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    # Manejo de fallo de verificación CSRF
    return HttpResponse("CSRF verification failed. Reason: %s" % reason)


@login_required
def some_view(request):
    # Vista protegida con login y manejo de roles de usuario
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
    # Configuración del idioma del usuario
    user_language = request.GET.get("language", "en")
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return redirect(request.META.get("HTTP_REFERER"))


def home(request):
    # Renderiza la página principal
    return render(request, "main/home.html")


def about(request):
    # Renderiza la página "Sobre nosotros"
    return render(request, "main/about.html")


def contact(request):
    # Maneja el formulario de contacto y envía un mensaje al administrador
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message_body = request.POST["message"]

        admin_user = User.objects.filter(groups__name="admin").first()
        if not admin_user:
            messages.error(request, "No admin found to send the message to.")
            return redirect("main:contact")

        Message.objects.create(
            sender=None if request.user.is_anonymous else request.user,
            recipient=admin_user,
            content=f"Name: {name}\nEmail: {email}\n\n{message_body}",
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("main:contact")

    return render(request, "main/contact.html")


def services(request):
    # Renderiza la página de servicios
    return render(request, "main/services.html")


def request_quote(request):
    # Renderiza la página de solicitud de cotización
    return render(request, "main/request_quote.html")


@csrf_protect
def register(request):
    # Maneja el registro de usuarios y asignación de roles
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")
            user.save()
            profile, created = Profile.objects.get_or_create(
                user=user, defaults={"role": role}
            )
            if not created:
                profile.role = role
                profile.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
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
    # Vista para mostrar mensajes del usuario
    messages = Message.objects.filter(recipient=request.user)
    return render(request, "messages_app/messages.html", {"messages": messages})


@login_required
def profile(request):
    # Vista para mostrar y editar el perfil del usuario
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
    # Vista para editar el perfil del usuario
    profile = Profile.objects.get(user=request.user)
    predefined_images = [
        f"assets/images/avatars/{image}"
        for image in os.listdir(
            os.path.join(settings.BASE_DIR, "its_portal/static/assets/images/avatars")
        )
    ]

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        current_password = request.POST.get("current_password")
        confirm_current_password = request.POST.get("confirm_current_password")

        if current_password != confirm_current_password:
            profile_form.add_error(None, "Current passwords do not match.")
        elif not request.user.check_password(current_password):
            profile_form.add_error(None, "Current password is incorrect.")
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile = profile_form.save(commit=False)

                if request.FILES.get("profile_picture"):
                    uploaded_file = request.FILES["profile_picture"]
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(
                        os.path.join("profile_images", uploaded_file.name),
                        uploaded_file,
                    )
                    profile.profile_picture = os.path.join(
                        "profile_images", uploaded_file.name
                    )
                    logger.info(
                        f"Saved file '{filename}' to 'media/profile_images' folder."
                    )

                elif request.POST.get("predefined_image"):
                    predefined_image = request.POST["predefined_image"]
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
                    os.makedirs(os.path.dirname(media_path), exist_ok=True)
                    if os.path.exists(predefined_image_path):
                        try:
                            shutil.copy(predefined_image_path, media_path)
                            profile.profile_picture = os.path.join(
                                "profile_images", os.path.basename(predefined_image)
                            )
                        except FileNotFoundError as e:
                            messages.error(
                                request, f"Error copying predefined image: {e}"
                            )
                    else:
                        messages.error(
                            request,
                            f"Predefined image not found: {predefined_image_path}",
                        )

                profile.save()
                messages.success(request, "Your profile has been updated!")
                return redirect("main:profile")
            else:
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
    # Vista para el dashboard del usuario según su rol
    profile = get_profile(request.user)
    context = {"profile": profile}

    if profile:
        if profile.role == "employee":
            topics = ForumTopic.objects.all()
            messages_list = Message.objects.filter(recipient=request.user)
            context.update({"topics": topics, "messages": messages_list})
            return render(request, "dashboard/employee_dashboard.html", context)
        elif profile.role == "client":
            return render(request, "dashboard/client_dashboard.html", context)
        elif profile.role == "admin":
            projects = Project.objects.all()
            messages_list = Message.objects.all()[:10]
            forum_posts = ForumPost.objects.select_related("topic").all()[:10]
            blog_posts = BlogPost.objects.all()[:10]
            context.update(
                {
                    "projects": projects,
                    "messages": messages_list,
                    "forum_posts": forum_posts,
                    "blog_posts": blog_posts,
                }
            )
            return render(request, "dashboard/admin_dashboard.html", context)
        else:
            return render(request, "main/user_dashboard.html", context)
    else:
        return redirect("main:create_profile")


def login_view(request):
    # Vista para manejar el login de usuarios
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
    # Vista para manejar el logout de usuarios
    logout(request)
    return redirect("main:home")


def test_media_static(request):
    # Vista de prueba para las carpetas media y static
    return render(
        request,
        "main/test_media_static.html",
        {
            "media_url": settings.MEDIA_URL,
            "static_url": settings.STATIC_URL,
        },
    )
