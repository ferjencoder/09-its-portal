# main/models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_ROLES = (
        ("user", "User"),
        ("employee", "Employee"),
        ("client", "Client"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile_main"
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default="user")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
        default="https://res.cloudinary.com/ferjen/image/upload/v1718991742/avatars/red_cuddly_iqxage.png",
    )

    def __str__(self):
        return f"{self.user.username} Profile"
