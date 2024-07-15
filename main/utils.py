# main/utils.py

from messages_app.models import Conversation
from .models import Profile


# Verifica si el usuario es administrador
def is_admin(user):
    return user.groups.filter(name="admin").exists()


# Verifica si el usuario pertenece al grupo "employee"
def is_employee(user):
    return user.groups.filter(name="employee").exists()


# Obtener perfil del usuario o devolver none si no existe
def get_profile(user):
    try:
        return user.profile_main
    except AttributeError:
        return None


# Crear u obtener una conversación entre dos usuarios
def get_or_create_conversation(user1, user2):
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
