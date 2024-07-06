# forum_app / tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ForumTopic, ForumPost

# setUp: Este método se llama antes de cada prueba. Configura un usuario de prueba, inicia sesión con ese usuario y crea un tema de foro de prueba.
# test_forum_view: Prueba que la vista del foro se cargue correctamente.
# test_create_topic_view: Prueba que se pueda crear un nuevo tema.
# test_topic_detail_view: Prueba que la vista de detalles del tema se cargue correctamente.
# test_create_post_view: Prueba que se pueda crear un nuevo post bajo un tema.
# test_post_detail_view: Prueba que la vista de detalles del post se cargue correctamente.
# test_reply_post_view: Prueba que se pueda responder a un post.
# test_search_functionality: Prueba que la funcionalidad de búsqueda filtre los temas correctamente.


class ForumAppTests(TestCase):

    def setUp(self):
        # Configurar un usuario de prueba
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()
        self.client.login(username="testuser", password="12345")

        # Crear un tema de foro de prueba
        self.topic = ForumTopic.objects.create(title="Test Topic", author=self.user)

    def test_forum_view(self):
        # Prueba para la vista del foro
        response = self.client.get(reverse("forum_app:forum"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum_app/forum.html")

    def test_create_topic_view(self):
        # Prueba para crear un nuevo tema
        response = self.client.post(
            reverse("forum_app:create_topic"),
            {
                "title": "New Topic",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(ForumTopic.objects.filter(title="New Topic").exists())

    def test_topic_detail_view(self):
        # Prueba para la vista de detalles del tema
        response = self.client.get(
            reverse("forum_app:topic_detail", args=[self.topic.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum_app/topic_detail.html")

    def test_create_post_view(self):
        # Prueba para crear un nuevo post
        response = self.client.post(
            reverse("forum_app:create_post", args=[self.topic.id]),
            {
                "content": "New Post Content",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(ForumPost.objects.filter(content="New Post Content").exists())

    def test_post_detail_view(self):
        # Prueba para la vista de detalles del post
        post = ForumPost.objects.create(
            topic=self.topic, author=self.user, content="Test Post Content"
        )
        response = self.client.get(reverse("forum_app:post_detail", args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum_app/post_detail.html")

    def test_reply_post_view(self):
        # Prueba para responder a un post
        post = ForumPost.objects.create(
            topic=self.topic, author=self.user, content="Test Post Content"
        )
        response = self.client.post(
            reverse("forum_app:reply_post", args=[post.id]),
            {
                "content": "Reply Post Content",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(ForumPost.objects.filter(content="Reply Post Content").exists())

    def test_search_functionality(self):
        # Prueba para la funcionalidad de búsqueda
        response = self.client.get(reverse("forum_app:forum"), {"search": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")
