# main/create_test_all_data.py

import os
import sys
import django

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()


# Función para ejecutar un script y verificar su resultado
def run_script(script_path):
    result = os.system(f"python {script_path}")
    if result != 0:
        print(f"Error: El script {script_path} falló.")
    else:
        print(f"Éxito: El script {script_path} se ejecutó correctamente.")


# Función principal para ejecutar todos los scripts de prueba
def main():
    # Rutas a los scripts individuales de prueba
    scripts = [
        "main/create_test_users.py",
        "blog_app/create_test_blog_data.py",
        "forum_app/create_test_forum_data.py",
        "messages_app/create_test_messages_data.py",
        "projects_app/create_test_projects_data.py",
        "communications_app/create_test_communications_data.py",  # Añadir este script
    ]

    # Ejecutar cada script
    for script in scripts:
        run_script(script)


# Punto de entrada principal del script
if __name__ == "__main__":
    main()
