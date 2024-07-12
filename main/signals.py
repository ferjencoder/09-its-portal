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
            print(f"Signal: Creating profile for new user {instance.username}")
    else:
        if hasattr(instance, "profile_main"):
            profile = instance.profile_main
            if not profile.role:
                # Attempt to set role based on user's group if not already set
                group = instance.groups.first()
                if group:
                    profile.role = group.name
                    profile.save()
                    print(
                        f"Signal: Setting role for existing user {instance.username} to {profile.role}"
                    )
            profile.save()
            print(f"Signal: Updating profile for existing user {instance.username}")


# Crear grupos por defecto si no existen
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "main":
        Group.objects.get_or_create(name="client")
        Group.objects.get_or_create(name="employee")
        Group.objects.get_or_create(name="admin")
