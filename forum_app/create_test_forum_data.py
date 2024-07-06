# forum_app/create_test_forum_data.py

import os
import sys
import django

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from forum_app.models import ForumTopic, ForumPost


def create_user(username, email, password):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        user.save()
    return user


def create_topic(title, author_username):
    author = User.objects.get(username=author_username)
    topic, created = ForumTopic.objects.get_or_create(title=title, author=author)
    return topic


def create_post(content, author_username, topic_title):
    author = User.objects.get(username=author_username)
    topic = ForumTopic.objects.get(title=topic_title)
    post, created = ForumPost.objects.get_or_create(
        content=content, author=author, topic=topic
    )
    return post


def main():
    # Crear usuarios
    create_user("admin1", "admin1@example.com", "admin1pass")
    create_user("employee1", "employee1@example.com", "employee1pass")
    create_user("client1", "client1@example.com", "client1pass")

    # Crear temas del foro
    create_topic("Technology Discussions", "admin1")
    create_topic("Health Discussions", "employee1")
    create_topic("Education Discussions", "client1")

    # Crear posts en los temas del foro
    create_post(
        "First post in Technology Discussions", "admin1", "Technology Discussions"
    )
    create_post("First post in Health Discussions", "employee1", "Health Discussions")
    create_post(
        "First post in Education Discussions", "client1", "Education Discussions"
    )
    create_post(
        "Second post in Technology Discussions", "admin1", "Technology Discussions"
    )
    create_post("Second post in Health Discussions", "employee1", "Health Discussions")
    create_post(
        "Second post in Education Discussions", "client1", "Education Discussions"
    )
    create_post(
        "Third post in Technology Discussions", "admin1", "Technology Discussions"
    )
    create_post("Third post in Health Discussions", "employee1", "Health Discussions")
    create_post(
        "Third post in Education Discussions", "client1", "Education Discussions"
    )


if __name__ == "__main__":
    main()
