# blog_app/views.py

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import BlogPostForm, CategoryForm
from .models import BlogPost, Category


# Verifica si el usuario pertenece al grupo "admin"
def is_admin(user):
    return user.groups.filter(name="admin").exists()


# Verifica si el usuario pertenece al grupo "employee"
def is_employee(user):
    return user.groups.filter(name="employee").exists()


# Crear una nueva categoría (solo admin)
@login_required
@user_passes_test(is_admin)
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"success": True, "message": "Categoría creada exitosamente."}
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Error al crear la categoría."}
            )
    return JsonResponse({"success": False, "message": "Método de solicitud inválido."})


# Lista de blogs con paginación y filtro por categoría
def blog_list(request):
    category_id = request.GET.get("category")
    if category_id:
        blog_posts = BlogPost.objects.filter(category_id=category_id).order_by(
            "-created_at"
        )
    else:
        blog_posts = BlogPost.objects.all().order_by("-created_at")

    paginator = Paginator(blog_posts, 3)  # Mostrar 3 posts por página
    page_number = request.GET.get("page")
    blog_posts = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        "blog_app/blog_list.html",
        {
            "blog_posts": blog_posts,
            "categories": categories,
            "selected_category": int(category_id) if category_id else None,
        },
    )


# Detalle de un blog específico
def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, "blog_app/blog_detail.html", {"post": post})


# Lista de blogs del empleado logueado con paginación
@login_required
def employee_blog_list(request):
    blog_posts = BlogPost.objects.filter(author=request.user).order_by("-created_at")

    paginator = Paginator(blog_posts, 3)  # Muestra 3 publicaciones por página
    page = request.GET.get("page")
    blog_posts = paginator.get_page(page)

    return render(
        request, "blog_app/employee_blog_list.html", {"blog_posts": blog_posts}
    )


# Crear una nueva entrada de blog
@login_required
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrada de blog creada exitosamente.")
            if is_admin(request.user):
                return redirect("blog_app:admin_blog_list")
            elif is_employee(request.user):
                return redirect("blog_app:employee_blog_list")
            else:
                return redirect("blog_app:blog_list")
        else:
            messages.error(request, "Error al crear la entrada de blog.")
    else:
        form = BlogPostForm()
    return render(request, "blog_app/create_blog_post.html", {"form": form})


# Lista de blogs para el admin con paginación y filtro por categoría
@login_required
@user_passes_test(is_admin, login_url="main:login")
def admin_blog_list(request):
    category_id = request.GET.get("category", None)
    if category_id:
        blog_posts = BlogPost.objects.filter(category_id=category_id).order_by(
            "-created_at"
        )
    else:
        blog_posts = BlogPost.objects.all().order_by("-created_at")

    categories = Category.objects.all()
    selected_category = int(category_id) if category_id else None

    paginator = Paginator(blog_posts, 3)  # Muestra 3 publicaciones por página
    page = request.GET.get("page")
    blog_posts = paginator.get_page(page)

    context = {
        "blog_posts": blog_posts,
        "categories": categories,
        "selected_category": selected_category,
    }
    return render(request, "blog_app/admin_blog.html", context)


# Editar una entrada de blog
@login_required
def edit_blog_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrada de blog actualizada exitosamente.")
            if is_admin(request.user):
                return redirect("blog_app:admin_blog_list")
            elif is_employee(request.user):
                return redirect("blog_app:employee_blog_list")
            else:
                return redirect("blog_app:blog_list")
        else:
            messages.error(request, "Error al actualizar la entrada de blog.")
    else:
        form = BlogPostForm(instance=post)
    return render(request, "blog_app/edit_blog_post.html", {"form": form, "post": post})


# Eliminar una entrada de blog
@login_required
def delete_blog_post(request, id):
    blog_post = get_object_or_404(BlogPost, id=id)
    if blog_post.author != request.user and not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":
        blog_post.delete()
        if is_admin(request.user):
            return redirect("blog_app:admin_blog_list")
        return redirect("blog_app:employee_blog_list")

    return render(request, "blog_app/delete_blog_post.html", {"blog_post": blog_post})


# Subir una imagen para el blog
@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        file_path = os.path.join("blog_images", uploaded_file.name)
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        file_url = default_storage.url(saved_path)
        return JsonResponse({"url": file_url})
    return JsonResponse({"error": {"message": "Error al subir la imagen"}})


# Lista pública de blogs con paginación y filtro por categoría
def blog_list_public(request):
    category_id = request.GET.get("category")
    if category_id:
        blog_posts = BlogPost.objects.filter(category_id=category_id).order_by(
            "-created_at"
        )
    else:
        blog_posts = BlogPost.objects.all().order_by("-created_at")

    paginator = Paginator(blog_posts, 3)  # Mostrar 3 posts por página
    page_number = request.GET.get("page")
    blog_posts = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(
        request,
        "blog_app/blog_list_public.html",
        {
            "blog_posts": blog_posts,
            "categories": categories,
            "selected_category": int(category_id) if category_id else None,
        },
    )
