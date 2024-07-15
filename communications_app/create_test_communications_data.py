# communications_app/create_test_communications_data.py

import os
import sys
import django
from django.utils.translation import gettext_lazy as _
from random import choice
from django.utils import timezone

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from main.models import ContactMessage, QuoteRequest  # Updated import path


# Función para crear mensajes de contacto de prueba
def create_test_contact_messages(users):
    messages = []
    for user in users:
        message = ContactMessage.objects.create(
            name=f"Contacto {user.username}",
            email=user.email,
            subject=f"Asunto de prueba {user.username}",
            message=f"Mensaje de prueba para {user.username}.",
            created_at=timezone.now(),
            read=choice([True, False]),
            archived=choice([True, False]),
            replied=choice([True, False]),
        )
        messages.append(message)
    return messages


# Función para crear solicitudes de cotización de prueba
def create_test_quote_requests(users):
    requests = []
    for user in users:
        request = QuoteRequest.objects.create(
            name=f"Solicitante {user.username}",
            email=user.email,
            phone="123-456-7890",
            company=f"Empresa {user.username}",
            service=choice(["Servicio A", "Servicio B", "Servicio C"]),
            message=f"Mensaje de solicitud de cotización para {user.username}.",
            created_at=timezone.now(),
            read=choice([True, False]),
            archived=choice([True, False]),
            replied=choice([True, False]),
        )
        requests.append(request)
    return requests


# Función principal para ejecutar todas las funciones de prueba
def main():
    users = User.objects.all()
    if users:
        create_test_contact_messages(users)
        create_test_quote_requests(users)
        print(_("Datos de prueba creados exitosamente."))
    else:
        print(_("No se encontraron usuarios para crear datos de prueba."))


if __name__ == "__main__":
    main()
