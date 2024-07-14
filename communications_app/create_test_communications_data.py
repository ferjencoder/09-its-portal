# communications_app/create_test_communications_data.py

import os
import sys
import django
from django.utils.translation import gettext_lazy as _
from random import choice, randint
from datetime import timedelta
from django.utils import timezone

# Configurar el directorio del proyecto y el módulo de configuración
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")

django.setup()

from django.contrib.auth.models import User
from communications_app.models import ContactMessage, QuoteRequest


# Función para obtener usuarios existentes
def get_existing_users():
    clients = User.objects.filter(groups__name="client")

    if not clients.exists():
        print(_("No se encontraron usuarios en el grupo 'client'."))
        return None

    return clients


# Función para crear mensajes de contacto de prueba
def create_test_contact_messages():
    messages = []
    subjects = ["Consulta general", "Soporte técnico", "Cotización", "Otros"]
    for i in range(1, 21):
        message = ContactMessage.objects.create(
            name=f"Cliente {i}",
            email=f"cliente{i}@example.com",
            subject=choice(subjects),
            message=f"Este es el mensaje de prueba número {i}.",
            created_at=timezone.now() - timedelta(days=randint(0, 30)),
            read=choice([True, False]),
            archived=choice([True, False]),
            replied=choice([True, False]),
        )
        messages.append(message)
    return messages


# Función para crear solicitudes de cotización de prueba
def create_test_quote_requests():
    requests = []
    services = ["Automation", "Data Visualization", "Project Management", "Training"]
    for i in range(1, 21):
        request = QuoteRequest.objects.create(
            name=f"Empresa {i}",
            email=f"empresa{i}@example.com",
            phone=f"+123456789{i}",
            company=f"Empresa {i} S.A.",
            service=choice(services),
            message=f"Mensaje de cotización para la empresa {i}.",
            created_at=timezone.now() - timedelta(days=randint(0, 30)),
            read=choice([True, False]),
            archived=choice([True, False]),
            replied=choice([True, False]),
        )
        requests.append(request)
    return requests


# Función principal para ejecutar todas las funciones de prueba
def main():
    clients = get_existing_users()
    if clients:
        create_test_contact_messages()
        create_test_quote_requests()
        print(_("Datos de prueba creados exitosamente."))
    else:
        print(
            _(
                "No se crearon datos de prueba debido a la falta de usuarios en los grupos especificados."
            )
        )


if __name__ == "__main__":
    main()
