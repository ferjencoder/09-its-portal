## forum_app/create_test_forum_data.py
import os
import sys
import django

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from forum_app.models import ForumTopic, ForumPost, ForumCategory


# Crear categoría si no existe
def create_category(name):
    category, created = ForumCategory.objects.get_or_create(name=name)
    return category


# Crear tema del foro
def create_topic(title, author_username, category_name):
    author = User.objects.get(username=author_username)
    category = create_category(category_name)
    topic, created = ForumTopic.objects.get_or_create(
        title=title, author=author, category=category
    )
    return topic


# Crear post en un tema del foro
def create_post(content, author_username, topic_title):
    author = User.objects.get(username=author_username)
    topic = ForumTopic.objects.get(title=topic_title)
    post, created = ForumPost.objects.get_or_create(
        content=content, author=author, topic=topic
    )
    return post


def main():
    # Crear categorías del foro
    categories = [
        "General Discussion",
        "Technical Support",
        "Announcements",
        "Feedback",
        "Special Interests",
    ]
    for category in categories:
        create_category(category)

    # Crear temas del foro
    create_topic("Welcome to the Forum", "admin1", "General Discussion")
    create_topic("Latest News", "admin1", "Announcements")

    # Crear posts en los temas del foro
    create_post(
        "Este es el primer post en la categoría de discusión general.",
        "admin1",
        "Welcome to the Forum",
    )
    create_post(
        "Este es un anuncio sobre las últimas noticias.", "admin1", "Latest News"
    )
    create_post(
        "Segundo post en la categoría de discusión general.",
        "employee1",
        "Welcome to the Forum",
    )
    create_post("Segundo post en anuncios.", "client1", "Latest News")


if __name__ == "__main__":
    main()


#
# import os
# import sys
# import django
#
## Agregar el directorio raíz del proyecto al sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
# django.setup()
#
# from django.contrib.auth.models import User
# from forum_app.models import ForumTopic, ForumPost, ForumCategory
#
#
## Crear usuario si no existe
# def create_user(username, email, password):
#    user, created = User.objects.get_or_create(
#        username=username, defaults={"email": email}
#    )
#    if created:
#        user.set_password(password)
#        user.save()
#    return user
#
#
## Crear categoría si no existe
# def create_category(name):
#    category, created = ForumCategory.objects.get_or_create(name=name)
#    return category
#
#
## Crear tema del foro
# def create_topic(title, author_username, category_name):
#    author = User.objects.get(username=author_username)
#    category = create_category(category_name)
#    topic, created = ForumTopic.objects.get_or_create(
#        title=title, author=author, category=category
#    )
#    return topic
#
#
## Crear post en un tema del foro
# def create_post(content, author_username, topic_title):
#    author = User.objects.get(username=author_username)
#    topic = ForumTopic.objects.get(title=topic_title)
#    post, created = ForumPost.objects.get_or_create(
#        content=content, author=author, topic=topic
#    )
#    return post
#
#
# def main():
#    # Crear usuarios
#    create_user("admin1", "admin1@example.com", "admin")
#    create_user("employee1", "employee1@example.com", "employee")
#    create_user("client1", "client1@example.com", "client")
#
#    # Crear temas del foro
#    create_topic("Automation Solutions", "admin1", "Automation Solutions")
#    create_topic("Data Visualization", "employee1", "Data Visualization")
#    create_topic("Project Management", "client1", "Project Management")
#    create_topic("Training Services", "admin1", "Training Services")
#
#    # Crear posts en los temas del foro
#    create_post("First post in Automation Solutions", "admin1", "Automation Solutions")
#    create_post("First post in Data Visualization", "employee1", "Data Visualization")
#    create_post("First post in Project Management", "client1", "Project Management")
#    create_post("First post in Training Services", "admin1", "Training Services")
#    create_post("Second post in Automation Solutions", "admin1", "Automation Solutions")
#    create_post("Second post in Data Visualization", "employee1", "Data Visualization")
#    create_post("Second post in Project Management", "client1", "Project Management")
#    create_post("Second post in Training Services", "admin1", "Training Services")
#    create_post("Third post in Automation Solutions", "admin1", "Automation Solutions")
#    create_post("Third post in Data Visualization", "employee1", "Data Visualization")
#    create_post("Third post in Project Management", "client1", "Project Management")
#    create_post("Third post in Training Services", "admin1", "Training Services")
#
#
# if __name__ == "__main__":
#    main()
