# main/reset_migrations_and_db.py

import os
import shutil
import sys
import subprocess

# Configurar el entorno del proyecto Django
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")

import django

django.setup()

from django.conf import settings


def delete_migrations_folders(app_names):
    # Eliminar las carpetas de migraciones para las aplicaciones especificadas
    for app_name in app_names:
        migrations_folder = os.path.join(project_root, app_name, "migrations")
        if os.path.exists(migrations_folder):
            print(f"Eliminando la carpeta de migraciones: {migrations_folder}")
            shutil.rmtree(migrations_folder)


def delete_database(db_path):
    # Eliminar el archivo de la base de datos si existe
    if os.path.exists(db_path):
        print(f"Eliminando la base de datos: {db_path}")
        os.remove(db_path)


def run_makemigrations(app_names):
    # Ejecutar makemigrations para cada aplicación especificada
    for app_name in app_names:
        os.system(f"python manage.py makemigrations {app_name}")


def run_migrate():
    # Ejecutar migrate para aplicar todas las migraciones
    os.system("python manage.py migrate")


# def create_superuser(username, email, password):
#    # Crear un superusuario usando subprocess.run
#    subprocess.run(
#        [
#            "python",
#            "manage.py",
#            "createsuperuser",
#            "--noinput",
#            "--username",
#            username,
#            "--email",
#            email,
#        ],
#        env={**os.environ, "DJANGO_SUPERUSER_PASSWORD": password},
#    )


def main():
    app_names = ["blog_app", "forum_app", "main", "messages_app", "projects_app"]
    db_path = os.path.join(project_root, "db.sqlite3")

    delete_migrations_folders(app_names)
    delete_database(db_path)
    run_makemigrations(app_names)
    run_migrate()

    # Crear superusuario
    # create_superuser("superadmin", "superadmin@gm.com", "superadminpass")


if __name__ == "__main__":
    main()
