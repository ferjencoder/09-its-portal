# main/apps.py

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        # Importa signals cuando la aplicación esté lista
        import main.signals
