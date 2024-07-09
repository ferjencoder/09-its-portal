# main/apps.py
# This file contains the configuration for the Django app. It's where the name of the app is defined and any app-specific configurations.

from django.apps import AppConfig


# Importa signals cuando la aplicación esté lista
class MainConfig(AppConfig):
    name = "main"

    def ready(self):
        import main.signals
