# messages_app / create_test_messages_data.py

import os
import sys
import django

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from messages_app.models import Message


def create_message(content, sender_username, recipient_username):
    # Crear mensaje si no existe
    sender = User.objects.get(username=sender_username)
    recipient = User.objects.get(username=recipient_username)
    message, created = Message.objects.get_or_create(
        content=content, sender=sender, recipient=recipient
    )
    return message


def main():
    # Crear mensajes entre usuarios
    create_message("Hola, soy admin1", "admin1", "employee1")
    create_message("Hola admin1, soy employee1", "employee1", "admin1")
    create_message("Hola, soy client1", "client1", "admin1")
    create_message("Hola client1, soy admin1", "admin1", "client1")
    create_message("Hola, soy employee1", "employee1", "client1")
    create_message("Hola employee1, soy client1", "client1", "employee1")


if __name__ == "__main__":
    main()


# sys.path.append: Se agrega el directorio raíz del proyecto al sys.path para que el script pueda encontrar las configuraciones y módulos de Django.
# os.environ.setdefault: Se configura la variable de entorno para usar el archivo de configuración de Django.
# django.setup: Se inicializa la configuración de Django.
# create_message: Se crea un mensaje si no existe.
# main: Se crean mensajes entre usuarios con mensajes en español para cumplir con i18n.
