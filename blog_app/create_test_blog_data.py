# blog_app/create_test_blog_data.py

import os
import sys
import django
import shutil

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from blog_app.models import BlogPost, BlogCategory


def create_category(name):
    # Crear o recuperar una categoría de blog por nombre.
    category, created = BlogCategory.objects.get_or_create(name=name)
    if created:
        print(f"Categoría creada: {name}")
    else:
        print(f"Categoría existente: {name}")
    return category


def create_blog_post(
    title, subtitle, body, author_username, category_name, image_name=None
):
    # Crear una entrada de blog con un autor y categoría específicos, y una imagen opcional.
    try:
        author = User.objects.get(username=author_username)
    except User.DoesNotExist:
        print(f"Error: El usuario {author_username} no existe.")
        return

    try:
        category = BlogCategory.objects.get(name=category_name)
    except BlogCategory.DoesNotExist:
        print(f"Error: La categoría {category_name} no existe.")
        return

    blog_post, created = BlogPost.objects.get_or_create(
        title=title,
        subtitle=subtitle,
        body=body,
        author=author,
        defaults={"category": category},
    )

    if created:
        print(f"Entrada de blog creada: {title}")
    else:
        print(f"Entrada de blog existente: {title}")

    if image_name:
        # Copiar imagen del blog
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "tests/images/", image_name
        )
        media_path = os.path.join("media/blog_images", image_name)
        if not os.path.exists(image_path):
            print(f"Error: La imagen {image_path} no existe.")
            return

        os.makedirs(os.path.dirname(media_path), exist_ok=True)
        shutil.copy(image_path, media_path)
        blog_post.image = os.path.join("blog_images", image_name)
        blog_post.save()
        print(f"Imagen para {title} guardada en {media_path}")

    return blog_post


def main():
    # Crear categorías del blog (servicios de ITS)
    categories = [
        "Automation Solutions",
        "Data Visualization",
        "Project Management",
        "Training Services",
    ]
    for category in categories:
        create_category(category)

    # Detalles de las entradas de blog
    blog_posts = [
        {
            "title": "First Automation Blog",
            "subtitle": "Subtitle for Automation Blog",
            "body": "Content of the first automation blog.",
            "author_username": "admin1",
            "category_name": "Automation Solutions",
            "image_name": "blog_image1.jpg",
        },
        {
            "title": "First Data Visualization Blog",
            "subtitle": "Subtitle for Data Visualization Blog",
            "body": "Content of the first data visualization blog.",
            "author_username": "employee1",
            "category_name": "Data Visualization",
            "image_name": "blog_image2.jpg",
        },
        {
            "title": "First Project Management Blog",
            "subtitle": "Subtitle for Project Management Blog",
            "body": "Content of the first project management blog.",
            "author_username": "client1",
            "category_name": "Project Management",
            "image_name": "blog_image3.jpg",
        },
        {
            "title": "First Training Blog",
            "subtitle": "Subtitle for Training Blog",
            "body": "Content of the first training blog.",
            "author_username": "admin2",
            "category_name": "Training Services",
            "image_name": "blog_image4.jpg",
        },
        {
            "title": "Second Automation Blog",
            "subtitle": "Subtitle for Automation Blog",
            "body": "Content of the second automation blog.",
            "author_username": "employee2",
            "category_name": "Automation Solutions",
            "image_name": "blog_image5.jpg",
        },
        {
            "title": "Second Data Visualization Blog",
            "subtitle": "Subtitle for Data Visualization Blog",
            "body": "Content of the second data visualization blog.",
            "author_username": "client2",
            "category_name": "Data Visualization",
            "image_name": "blog_image6.jpg",
        },
        {
            "title": "Second Project Management Blog",
            "subtitle": "Subtitle for Project Management Blog",
            "body": "Content of the second project management blog.",
            "author_username": "admin3",
            "category_name": "Project Management",
            "image_name": "blog_image7.jpg",
        },
        {
            "title": "Second Training Blog",
            "subtitle": "Subtitle for Training Blog",
            "body": "Content of the second training blog.",
            "author_username": "employee3",
            "category_name": "Training Services",
            "image_name": "blog_image8.jpg",
        },
        {
            "title": "Third Automation Blog",
            "subtitle": "Subtitle for Automation Blog",
            "body": "Content of the third automation blog.",
            "author_username": "client3",
            "category_name": "Automation Solutions",
            "image_name": "blog_image9.jpg",
        },
        {
            "title": "Third Data Visualization Blog",
            "subtitle": "Subtitle for Data Visualization Blog",
            "body": "Content of the third data visualization blog.",
            "author_username": "admin4",
            "category_name": "Data Visualization",
            "image_name": "blog_image10.jpg",
        },
    ]

    # Crear entradas de blog
    for post in blog_posts:
        create_blog_post(**post)


if __name__ == "__main__":
    main()
