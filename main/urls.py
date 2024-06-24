# main/urls.py

from django.urls import path, include
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("set_language/", views.set_language, name="set_language"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("services/", views.services, name="services"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("request_quote/", views.request_quote, name="request_quote"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("forum/", include("forum_app.urls", namespace="forum_app")),
    path("messages/", include("messages_app.urls", namespace="messages_app")),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
