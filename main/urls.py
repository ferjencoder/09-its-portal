# main/urls.py

from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),  # Página principal
    path("set_language/", include("django.conf.urls.i18n")),  # Configuración de idioma
    path(
        "clear_welcome_modal_flag/",
        views.clear_welcome_modal_flag,
        name="clear_welcome_modal_flag",
    ),  # Mensaje de bienvenida
    path("about/", views.about, name="about"),  # Página "About Us"
    path("contact/", views.contact, name="contact"),  # Página de contacto
    path("services/", views.services, name="services"),  # Página de servicios
    path("register/", views.register, name="register"),  # Registro de usuario
    path("profile/", views.profile, name="profile"),  # Perfil de usuario
    path("edit_profile/", views.edit_profile, name="edit_profile"),  # Editar perfil
    path(
        "request_quote/", views.request_quote, name="request_quote"
    ),  # Solicitud de cotización
    path("dashboard/", views.dashboard, name="dashboard"),  # Dashboard principal
    path("forum/", include("forum_app.urls", namespace="forum_app")),  # URLs del foro
    path(
        "messages/", include("messages_app.urls", namespace="messages_app")
    ),  # URLs de mensajes
    path("login/", views.login_view, name="login"),  # Iniciar sesión
    path("logout/", views.logout_view, name="logout"),  # Cerrar sesión
    path(
        "test_media_static/", views.test_media_static, name="test_media_static"
    ),  # Prueba de media y static
]
