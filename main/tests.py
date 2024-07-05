# main/test.py

from django.test import TestCase
from django.contrib.auth.models import User, Group
from main.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile


class UserCreationTests(TestCase):

    def setUp(self):
        # Crear grupos de roles
        self.create_group("admin")
        self.create_group("employee")
        self.create_group("client")

        # Crear usuarios de prueba con imagen de perfil
        self.create_user("admin1", "admin1@example.com", "admin", "admin")
        self.create_user("admin2", "admin2@example.com", "admin", "admin")
        self.create_user("employee1", "employee1@example.com", "employee", "employee")
        self.create_user("employee2", "employee2@example.com", "employee", "employee")
        self.create_user("client1", "client1@example.com", "client", "client")
        self.create_user("client2", "client2@example.com", "client", "client")

    def create_group(self, name):
        group, created = Group.objects.get_or_create(name=name)
        return group

    def create_user(self, username, email, password, group_name):
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            user.set_password(password)
            user.save()

        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        profile = Profile.objects.get_or_create(
            user=user, defaults={"role": group_name}
        )[0]
        # Asignar imagen de perfil ficticia
        profile.profile_picture = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg"
        )
        profile.role = group_name  # Asegurarse de que el rol se asigne correctamente
        profile.save()

    def test_users_creation(self):
        # Verificar que los usuarios se crearon correctamente
        self.verify_user("admin1", "admin1@example.com", "admin")
        self.verify_user("admin2", "admin2@example.com", "admin")
        self.verify_user("employee1", "employee1@example.com", "employee")
        self.verify_user("employee2", "employee2@example.com", "employee")
        self.verify_user("client1", "client1@example.com", "client")
        self.verify_user("client2", "client2@example.com", "client")

    def verify_user(self, username, email, role):
        user = User.objects.get(username=username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(role))
        self.assertTrue(user.groups.filter(name=role).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.role, role)
        self.assertTrue(
            profile.profile_picture
        )  # Verificar que la imagen de perfil esté asignada
