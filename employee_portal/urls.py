# employee_portal/urls.py

from django.urls import path
from . import views

app_name = "employee_portal"

urlpatterns = [
    path("", views.employee_dashboard, name="employee_dashboard"),
    path("dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("documents/", views.documents, name="documents"),
    path("approve_work/", views.approve_work, name="approve_work"),
    path("create_blog_post/", views.create_blog_post, name="create_blog_post"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_employee_profile"),
]
