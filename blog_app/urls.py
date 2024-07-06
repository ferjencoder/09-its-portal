# blog_app/urls.py

from django.urls import path
from .views import upload_image
from . import views

app_name = "blog_app"

urlpatterns = [
    # Lista de blogs públicos
    path("", views.blog_list_public, name="blog_list_public"),
    # Lista de blogs
    path("blog/", views.blog_list, name="blog_list"),
    # Detalle de un blog
    path("<int:id>/", views.blog_detail, name="blog_detail"),
    # Lista de blogs para empleados
    path("employee/", views.employee_blog_list, name="employee_blog_list"),
    # Crear un blog post
    path("create/", views.create_blog_post, name="create_blog_post"),
    # Lista de blogs para admin
    path("admin/", views.admin_blog_list, name="admin_blog_list"),
    # Editar un blog post
    path("edit/<int:id>/", views.edit_blog_post, name="edit_blog_post"),
    # Eliminar un blog post
    path("delete/<int:id>/", views.delete_blog_post, name="delete_blog_post"),
    # Subir imagen
    path("upload-image/", upload_image, name="upload_image"),
    # Crear categoría
    path("category/create/", views.create_category, name="create_category"),
]
