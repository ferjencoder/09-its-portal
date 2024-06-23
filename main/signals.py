# main/signals.py

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile
from .utils import get_profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile_main.save()


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "main":
        Group.objects.get_or_create(name="client")
        Group.objects.get_or_create(name="employee")
        Group.objects.get_or_create(name="admin")
