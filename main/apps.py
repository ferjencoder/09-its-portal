# main/apps.py
# Configuración de la aplicación Django. Define el nombre de la app y configuraciones específicas.

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        import main.signals
