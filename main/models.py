# main/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# La imagen se subirá a MEDIA_ROOT/profile_images/user_<id>/<filename>
def user_directory_path(instance, filename):
    return f"profile_images/user_{instance.user.id}/{filename}"


# Modelo de perfil de usuario con roles y detalles adicionales
class Profile(models.Model):
    USER_ROLES = (
        ("admin", _("Admin")),
        ("client", _("Client")),
        ("employee", _("Employee")),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_main"
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default="")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/default_avatar.png",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.user.is_superuser and not self.role:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"


class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    service = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"Quote Request from {self.name} - {self.email}"
