# main/create_test_users.py

import os
import sys
import django
import shutil

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User, Group
from main.models import Profile


def create_group(name):
    group, created = Group.objects.get_or_create(name=name)
    return group


def create_user(username, email, password, group_name, image_name):
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(
            password
        )  # las passwords son admin, employee y client respectivamente
        user.save()

    group = Group.objects.get(name=group_name)
    user.groups.add(group)
    profile = Profile.objects.get_or_create(user=user, defaults={"role": group_name})[0]

    # Copiar imagen de perfil predefinida
    image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tests/images/", image_name
    )
    media_path = os.path.join("media/profile_images", image_name)
    if not os.path.exists(image_path):
        print(f"Error: La imagen {image_path} no existe.")
        return

    os.makedirs(os.path.dirname(media_path), exist_ok=True)
    shutil.copy(image_path, media_path)
    profile.profile_picture = os.path.join("profile_images", image_name)
    profile.role = group_name  # Asegurarse de que el rol se asigne correctamente
    profile.save()


def main():
    # Crear grupos de roles
    create_group("admin")
    create_group("employee")
    create_group("client")

    # Crear usuarios de prueba con imagen de perfil predefinida
    create_user("admin1", "admin1@example.com", "admin", "admin", "admin1.png")
    create_user("admin2", "admin2@example.com", "admin", "admin", "admin2.png")
    create_user(
        "employee1", "employee1@example.com", "employee", "employee", "employee1.png"
    )
    create_user(
        "employee2", "employee2@example.com", "employee", "employee", "employee2.png"
    )
    create_user("client1", "client1@example.com", "client", "client", "client1.png")
    create_user("client2", "client2@example.com", "client", "client", "client2.png")


if __name__ == "__main__":
    main()
