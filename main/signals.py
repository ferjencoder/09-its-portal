# main/signals.py
# This file is used to define signals and signal handlers. Signals allow certain senders to notify a set of receivers when certain actions have taken place.

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile


# Crear o actualizar perfil de usuario al guardar el usuario
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)


# Crear grupos por defecto si no existen
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "main":
        Group.objects.get_or_create(name="user")
        Group.objects.get_or_create(name="client")
        Group.objects.get_or_create(name="employee")
        Group.objects.get_or_create(name="admin")
