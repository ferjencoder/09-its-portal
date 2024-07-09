# main/apps.py

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    # Importa signals cuando la aplicación esté lista
    def ready(self):
        import main.signals
