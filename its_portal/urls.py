# its_portal/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from main import views as main_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("its_admin/", include("its_admin.urls")),
    path("messages/", include("messages_app.urls")),
    path("forum/", include("forum_app.urls")),
    path("client/", include("client_portal.urls")),
    path("employee/", include("employee_portal.urls")),
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls", namespace="blog")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="main/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", main_views.profile, name="profile"),
    path("request_quote/", main_views.request_quote, name="request_quote"),
    path("dashboard/", main_views.dashboard, name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
