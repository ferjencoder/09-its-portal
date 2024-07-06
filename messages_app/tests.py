# messages_app/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message


class MessagesAppTests(TestCase):

    # Configuración inicial para utilizar usuarios y mensajes de prueba existentes
    def setUp(self):
        self.admin1 = User.objects.create_user(username="admin1", password="admin1pass")
        self.employee1 = User.objects.create_user(
            username="employee1", password="employee1pass"
        )
        self.client1 = User.objects.create_user(
            username="client1", password="client1pass"
        )

        self.message1 = Message.objects.create(
            sender=self.admin1,
            recipient=self.employee1,
            content="Hello, this is admin1",
        )
        self.message2 = Message.objects.create(
            sender=self.employee1,
            recipient=self.admin1,
            content="Hi admin1, this is employee1",
        )
        self.message3 = Message.objects.create(
            sender=self.client1, recipient=self.admin1, content="Hello, this is client1"
        )
        self.message4 = Message.objects.create(
            sender=self.admin1,
            recipient=self.client1,
            content="Hi client1, this is admin1",
        )

    # Prueba de la vista predeterminada de mensajes
    def test_default_messages_view(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.get(reverse("messages_app:default_messages_view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/messages.html")
        self.assertContains(response, "employee1")
        self.assertContains(response, "client1")

    # Prueba de la vista de mensajes de una conversación específica
    def test_messages_view(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.get(
            reverse("messages_app:messages_view", args=[self.employee1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/messages.html")
        self.assertContains(response, "Hello, this is admin1")
        self.assertContains(response, "Hi admin1, this is employee1")

    # Prueba del envío de un mensaje
    def test_send_message(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.post(
            reverse("messages_app:send_message", args=[self.employee1.id]),
            {"content": "New message from admin1"},
        )
        self.assertEqual(response.status_code, 302)  # Redirección después del envío
        self.assertTrue(
            Message.objects.filter(content="New message from admin1").exists()
        )

    # Prueba de la eliminación de un mensaje
    def test_delete_message(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.post(
            reverse("messages_app:delete_message", args=[self.message1.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirección después de la eliminación
        self.assertFalse(Message.objects.filter(id=self.message1.id).exists())

    # Prueba de la edición de un mensaje
    def test_edit_message(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.post(
            reverse("messages_app:edit_message", args=[self.message1.id]),
            {"content": "Updated message from admin1"},
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de la edición
        self.assertTrue(
            Message.objects.filter(content="Updated message from admin1").exists()
        )

    # Prueba de la búsqueda de mensajes
    def test_search_messages(self):
        self.client.login(username="admin1", password="admin1pass")
        response = self.client.get(
            reverse("messages_app:search_messages"), {"q": "admin1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messages_app/search_results.html")
        self.assertContains(response, "Hello, this is admin1")
        self.assertContains(response, "Hi admin1, this is employee1")
