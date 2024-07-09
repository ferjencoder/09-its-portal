# main/models.py
# This file contains the models for the Django app. Models define the structure of the database tables.

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# La imagen se subirá a MEDIA_ROOT/profile_images/user_<id>/<filename>
def user_directory_path(instance, filename):
    return f"profile_images/user_{instance.user.id}/{filename}"


# Modelo de perfil de usuario con roles y detalles adicionales
class Profile(models.Model):
    USER_ROLES = (
        ("user", _("User")),
        ("employee", _("Employee")),
        ("client", _("Client")),
        ("admin", _("Admin")),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", unique=True
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default="user")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default="profile_images/default_avatar.png",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} Profile"
