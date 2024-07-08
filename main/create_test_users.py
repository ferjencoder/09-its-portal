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
    # Crear o recuperar un grupo de usuarios por nombre
    group, created = Group.objects.get_or_create(name=name)
    return group


def create_user(username, email, password, group_name, image_name):
    # Crear un usuario y asignarlo a un grupo específico, con una imagen de perfil predefinida
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)  # Establecer la contraseña del usuario
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

    # Preguntar al usuario si desea crear nuevos usuarios
    create_new_users = input("¿Desea crear nuevos usuarios? (s/n): ").lower()
    if create_new_users == "s":
        num_users = int(input("Ingrese el número de usuarios para crear por rol: "))

        for i in range(1, num_users + 1):
            create_user(
                f"admin{i}", f"admin{i}@gm.com", "admin", "admin", f"admin{i}.png"
            )
            create_user(
                f"employee{i}",
                f"employee{i}@gm.com",
                "employee",
                "employee",
                f"employee{i}.png",
            )
            create_user(
                f"client{i}", f"client{i}@gm.com", "client", "client", f"client{i}.png"
            )

        # Ejecutar el script de creación de datos de prueba del foro
        os.system("python forum_app/create_test_forum_data.py")
    else:
        print("No se crearán nuevos usuarios.")


if __name__ == "__main__":
    main()
