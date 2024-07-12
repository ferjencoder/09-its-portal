# main/tests.py

from django.test import TestCase
from django.contrib.auth.models import User, Group
from main.models import Profile
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserCreationTests(TestCase):

    def setUp(self):
        # Crear grupos de roles
        self.create_group("admin")
        self.create_group("employee")
        self.create_group("client")

    def create_group(self, name):
        group, created = Group.objects.get_or_create(name=name)
        return group

    def test_registration_view(self):
        url = reverse("main:register")
        response = self.client.post(
            url,
            {
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@example.com",
                "password1": "testpassword123",
                "password2": "testpassword123",
                "role": "admin",
            },
        )

        # Verificar que el usuario sea redirigido después del registro
        self.assertEqual(response.status_code, 302)

        # Verificar que el usuario se haya creado correctamente
        user = get_user_model().objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertTrue(user.groups.filter(name="admin").exists())

        # Adding more debug output to understand what went wrong
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.role, "admin")
