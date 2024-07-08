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
from blog_app.models import BlogPost, Category


def create_category(name):
    # Crear o recuperar una categoría de blog por nombre.
    category, created = Category.objects.get_or_create(name=name)
    return category


def create_blog_post(
    title, subtitle, body, author_username, category_name, image_name=None
):
    # Crear una entrada de blog con un autor y categoría específicos, y una imagen opcional.
    author = User.objects.get(username=author_username)
    category = Category.objects.get(name=category_name)
    blog_post, created = BlogPost.objects.get_or_create(
        title=title,
        subtitle=subtitle,
        body=body,
        author=author,
        defaults={"category": category},
    )

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

    return blog_post


def main():
    # Crear categorias del blog (servicios de ITS)
    create_category("Automation Solutions")
    create_category("Data Visualization")
    create_category("Project Management")
    create_category("Training Services")

    # Crear entradas de blog
    create_blog_post(
        "First Automation Blog",
        "Subtitle for Automation Blog",
        "Content of the first automation blog.",
        "admin1",
        "Automation Solutions",
        "blog_image1.jpg",
    )
    create_blog_post(
        "First Data Visualization Blog",
        "Subtitle for Data Visualization Blog",
        "Content of the first data visualization blog.",
        "employee1",
        "Data Visualization",
        "blog_image2.jpg",
    )
    create_blog_post(
        "First Project Management Blog",
        "Subtitle for Project Management Blog",
        "Content of the first project management blog.",
        "client1",
        "Project Management",
        "blog_image3.jpg",
    )
    create_blog_post(
        "First Training Blog",
        "Subtitle for Training Blog",
        "Content of the first training blog.",
        "admin2",
        "Training Services",
        "blog_image4.jpg",
    )
    create_blog_post(
        "Second Automation Blog",
        "Subtitle for Automation Blog",
        "Content of the second automation blog.",
        "employee2",
        "Automation Solutions",
        "blog_image5.jpg",
    )
    create_blog_post(
        "Second Data Visualization Blog",
        "Subtitle for Data Visualization Blog",
        "Content of the second data visualization blog.",
        "client2",
        "Data Visualization",
        "blog_image6.jpg",
    )
    create_blog_post(
        "Second Project Management Blog",
        "Subtitle for Project Management Blog",
        "Content of the second project management blog.",
        "admin3",
        "Project Management",
        "blog_image7.jpg",
    )
    create_blog_post(
        "Second Training Blog",
        "Subtitle for Training Blog",
        "Content of the second training blog.",
        "employee3",
        "Training Services",
        "blog_image8.jpg",
    )
    create_blog_post(
        "Third Automation Blog",
        "Subtitle for Automation Blog",
        "Content of the third automation blog.",
        "client3",
        "Automation Solutions",
        "blog_image9.jpg",
    )
    create_blog_post(
        "Third Data Visualization Blog",
        "Subtitle for Data Visualization Blog",
        "Content of the third data visualization blog.",
        "admin4",
        "Data Visualization",
        "blog_image10.jpg",
    )


if __name__ == "__main__":
    main()
