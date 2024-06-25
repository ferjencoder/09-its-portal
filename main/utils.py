# main/utils.py

from .models import Profile


def get_profile(user):
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None
