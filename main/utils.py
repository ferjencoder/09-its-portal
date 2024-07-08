# main/utils.py

from .models import Profile
from messages_app.models import Conversation


def get_profile(user):
    # Obtener perfil del usuario o devolver none si no existe
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None


def get_or_create_conversation(user1, user2):
    # Asegura que se crean conversaciones una vez para cada par de usuarios
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
