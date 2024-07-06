# blog_app/urls.py

from django.urls import path
from .views import upload_image
from . import views

app_name = "blog_app"

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:id>/", views.blog_detail, name="blog_detail"),
    path("employee/", views.employee_blog_list, name="employee_blog_list"),
    path("create/", views.create_blog_post, name="create_blog_post"),
    path("admin/", views.admin_blog_list, name="admin_blog_list"),
    path("edit/<int:id>/", views.edit_blog_post, name="edit_blog_post"),
    path("delete/<int:id>/", views.delete_blog_post, name="delete_blog_post"),
    path("upload-image/", upload_image, name="upload_image"),
]
