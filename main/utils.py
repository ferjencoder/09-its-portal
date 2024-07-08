# main/utils.py

from .models import Profile


def get_profile(user):
    # Obtener perfil del usuario o devolver none si no existe
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None
