# communications_app/tests.py

from django.test import TestCase
from django.utils import timezone
from .models import ContactMessage, QuoteRequest


class ContactMessageModelTest(TestCase):
    # Configuración inicial para las pruebas
    def setUp(self):
        self.contact_message = ContactMessage.objects.create(
            name="Test User",
            email="testuser@example.com",
            subject="Test Subject",
            message="This is a test message.",
            created_at=timezone.now(),
        )

    # Prueba de creación de mensaje de contacto
    def test_contact_message_creation(self):
        self.assertEqual(self.contact_message.name, "Test User")
        self.assertEqual(self.contact_message.email, "testuser@example.com")
        self.assertEqual(self.contact_message.subject, "Test Subject")
        self.assertEqual(self.contact_message.message, "This is a test message.")
        self.assertFalse(self.contact_message.read)
        self.assertFalse(self.contact_message.archived)
        self.assertFalse(self.contact_message.replied)

    # Prueba de actualización de mensaje de contacto
    def test_contact_message_update(self):
        self.contact_message.read = True
        self.contact_message.save()
        updated_message = ContactMessage.objects.get(id=self.contact_message.id)
        self.assertTrue(updated_message.read)


class QuoteRequestModelTest(TestCase):
    # Configuración inicial para las pruebas
    def setUp(self):
        self.quote_request = QuoteRequest.objects.create(
            name="Test Company",
            email="testcompany@example.com",
            phone="+123456789",
            company="Test Company S.A.",
            service="Automation",
            message="This is a test quote request.",
            created_at=timezone.now(),
        )

    # Prueba de creación de solicitud de cotización
    def test_quote_request_creation(self):
        self.assertEqual(self.quote_request.name, "Test Company")
        self.assertEqual(self.quote_request.email, "testcompany@example.com")
        self.assertEqual(self.quote_request.phone, "+123456789")
        self.assertEqual(self.quote_request.company, "Test Company S.A.")
        self.assertEqual(self.quote_request.service, "Automation")
        self.assertEqual(self.quote_request.message, "This is a test quote request.")
        self.assertFalse(self.quote_request.read)
        self.assertFalse(self.quote_request.archived)
        self.assertFalse(self.quote_request.replied)

    # Prueba de actualización de solicitud de cotización
    def test_quote_request_update(self):
        self.quote_request.replied = True
        self.quote_request.save()
        updated_request = QuoteRequest.objects.get(id=self.quote_request.id)
        self.assertTrue(updated_request.replied)
