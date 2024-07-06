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
    category, created = Category.objects.get_or_create(name=name)
    return category


def create_blog_post(
    title, subtitle, body, author_username, category_name, image_name=None
):
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
    # Crear categorías de blog
    create_category("Technology")
    create_category("Health")
    create_category("Education")

    # Crear entradas de blog
    create_blog_post(
        "First Technology Blog",
        "Subtitle for Technology Blog",
        "Content of the first technology blog.",
        "admin1",
        "Technology",
        "tech_blog.jpg",
    )
    create_blog_post(
        "First Health Blog",
        "Subtitle for Health Blog",
        "Content of the first health blog.",
        "employee1",
        "Health",
        "health_blog.jpg",
    )
    create_blog_post(
        "First Education Blog",
        "Subtitle for Education Blog",
        "Content of the first education blog.",
        "client1",
        "Education",
        "education_blog.jpg",
    )
    create_blog_post(
        "Second Technology Blog",
        "Subtitle for Technology Blog",
        "Content of the first technology blog.",
        "admin1",
        "Technology",
        "tech_blog.jpg",
    )
    create_blog_post(
        "Second Health Blog",
        "Subtitle for Health Blog",
        "Content of the second health blog.",
        "employee1",
        "Health",
        "health_blog.jpg",
    )
    create_blog_post(
        "Second Education Blog",
        "Subtitle for Education Blog",
        "Content of the second education blog.",
        "client1",
        "Education",
        "education_blog.jpg",
    )
    create_blog_post(
        "Third Technology Blog",
        "Subtitle for Technology Blog",
        "Content of the third technology blog.",
        "admin1",
        "Technology",
        "tech_blog.jpg",
    )
    create_blog_post(
        "Third Health Blog",
        "Subtitle for Health Blog",
        "Content of the third health blog.",
        "employee1",
        "Health",
        "health_blog.jpg",
    )
    create_blog_post(
        "Third Education Blog",
        "Subtitle for Education Blog",
        "Content of the third education blog.",
        "client1",
        "Education",
        "education_blog.jpg",
    )
    create_blog_post(
        "Fourth Technology Blog",
        "Subtitle for Technology Blog",
        "Content of the fourth technology blog.",
        "admin1",
        "Technology",
        "tech_blog.jpg",
    )
    create_blog_post(
        "Fourth Health Blog",
        "Subtitle for Health Blog",
        "Content of the fourth health blog.",
        "employee1",
        "Health",
        "health_blog.jpg",
    )
    create_blog_post(
        "Fourth Education Blog",
        "Subtitle for Education Blog",
        "Content of the fourth education blog.",
        "client1",
        "Education",
        "education_blog.jpg",
    )


if __name__ == "__main__":
    main()
