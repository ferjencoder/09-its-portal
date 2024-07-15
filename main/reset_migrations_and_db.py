# main/reset_migrations_and_db.py

import os
import shutil
import sys

# Configurar el entorno del proyecto Django
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")

import django

django.setup()


def delete_migrations_folders(app_names):
    # Eliminar carpetas de migraciones
    for app_name in app_names:
        migrations_folder = os.path.join(project_root, app_name, "migrations")
        if os.path.exists(migrations_folder):
            print(f"Eliminando carpeta de migraciones: {migrations_folder}")
            shutil.rmtree(migrations_folder)


def delete_database(db_path):
    # Eliminar archivo de base de datos
    if os.path.exists(db_path):
        print(f"Eliminando base de datos: {db_path}")
        os.remove(db_path)


def run_makemigrations(app_names):
    # Ejecutar makemigrations para cada aplicación
    for app_name in app_names:
        os.system(f"python manage.py makemigrations {app_name}")


def run_migrate():
    # Ejecutar migrate
    os.system("python manage.py migrate")


def main():
    app_names = [
        "blog_app",
        "communications_app",
        "forum_app",
        "main",
        "messages_app",
        "projects_app",
    ]
    db_path = os.path.join(project_root, "db.sqlite3")

    delete_migrations_folders(app_names)
    delete_database(db_path)
    run_makemigrations(app_names)
    run_migrate()


if __name__ == "__main__":
    main()
