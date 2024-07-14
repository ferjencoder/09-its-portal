# main/signals.py
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile


# Crear o actualizar perfil de usuario al guardar el usuario
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
    else:
        if hasattr(instance, "profile_main"):
            profile = instance.profile_main
            if not profile.role:
                # Intentar establecer el rol según el grupo del usuario si no está ya definido
                group = instance.groups.first()
                if group:
                    profile.role = group.name
                    profile.save()
            profile.save()


# Crear grupos por defecto si no existen
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "main":
        Group.objects.get_or_create(name="client")
        Group.objects.get_or_create(name="employee")
        Group.objects.get_or_create(name="admin")
