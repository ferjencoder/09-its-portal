# messages_app/create_test_messages_data.py

import os
import sys
import django

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "its_portal.settings")
django.setup()

from django.contrib.auth.models import User
from messages_app.models import Message, Conversation


def get_or_create_conversation(user1, user2):
    # Asegurarse de que las conversaciones se creen solo una vez para cada par de usuarios
    conversation = (
        Conversation.objects.filter(participants=user1)
        .filter(participants=user2)
        .first()
    )
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(user1, user2)
        conversation.save()
    return conversation


def create_message(content, sender_username, recipient_username):
    # Crear un mensaje dentro de una conversación
    sender = User.objects.get(username=sender_username)
    recipient = User.objects.get(username=recipient_username)
    conversation = get_or_create_conversation(sender, recipient)
    Message.objects.create(
        content=content, sender=sender, recipient=recipient, conversation=conversation
    )


def main():
    # Crear mensajes entre usuarios
    users = User.objects.all()

    for sender in users:
        for recipient in users:
            if sender != recipient:
                content = f"Hola {recipient.username}, soy {sender.username}"
                create_message(content, sender.username, recipient.username)


if __name__ == "__main__":
    main()
