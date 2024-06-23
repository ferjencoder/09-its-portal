from .models import Profile


def get_profile(user):
    try:
        return user.profile_main
    except Profile.DoesNotExist:
        return None
