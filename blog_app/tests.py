# blog_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import BlogPost, Category
from .forms import BlogPostForm, CategoryForm
from django.db.utils import IntegrityError


class BlogAppTests(TestCase):

    def setUp(self):
        # Crear usuario y grupos
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123"
        )
        self.employee_user = User.objects.create_user(
            username="employee", password="employee123"
        )

        # Verificar y crear grupo admin si no existe
        try:
            self.admin_group, created = Group.objects.get_or_create(name="admin")
        except IntegrityError:
            self.admin_group = Group.objects.get(name="admin")

        # Verificar y crear grupo employee si no existe
        try:
            self.employee_group, created = Group.objects.get_or_create(name="employee")
        except IntegrityError:
            self.employee_group = Group.objects.get(name="employee")

        self.admin_user.groups.add(self.admin_group)
        self.employee_user.groups.add(self.employee_group)

        # Crear categorias
        self.category = Category.objects.create(name="Test Category")

        # Crear un blog post
        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            subtitle="Test Subtitle",
            body="Test Body",
            author=self.admin_user,
            category=self.category,
        )

        self.client = Client()

    def test_create_category(self):
        # Probar la creación de una categoría
        self.client.login(username="admin", password="admin123")
        response = self.client.post(
            reverse("blog_app:create_category"), {"name": "New Category"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_blog_post(self):
        # Probar la creación de un blog post
        self.client.login(username="admin", password="admin123")
        form_data = {
            "title": "New Post",
            "subtitle": "New Subtitle",
            "body": "New Body",
            "author": self.admin_user.id,
            "category": self.category.id,
        }
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse("blog_app:create_blog_post"), form_data)
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(BlogPost.objects.count(), 2)

    def test_blog_list_view(self):
        # Probar la vista de lista de blogs
        response = self.client.get(reverse("blog_app:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_blog_detail_view(self):
        # Probar la vista de detalle de un blog
        response = self.client.get(
            reverse("blog_app:blog_detail", args=[self.blog_post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_edit_blog_post(self):
        # Probar la edición de un blog post
        self.client.login(username="admin", password="admin123")
        form_data = {
            "title": "Updated Post",
            "subtitle": "Updated Subtitle",
            "body": "Updated Body",
            "author": self.admin_user.id,
            "category": self.category.id,
        }
        response = self.client.post(
            reverse("blog_app:edit_blog_post", args=[self.blog_post.id]), form_data
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de editar
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, "Updated Post")

    def test_delete_blog_post(self):
        # Probar la eliminación de un blog post
        self.client.login(username="admin", password="admin123")
        response = self.client.post(
            reverse("blog_app:delete_blog_post", args=[self.blog_post.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_employee_blog_list_view(self):
        # Probar la vista de lista de blogs para empleados
        self.client.login(username="employee", password="employee123")
        response = self.client.get(reverse("blog_app:employee_blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blog posts found.")

    def test_admin_blog_list_view(self):
        # Probar la vista de lista de blogs para admin
        self.client.login(username="admin", password="admin123")
        response = self.client.get(reverse("blog_app:admin_blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_upload_image(self):
        # Probar la subida de una imagen
        self.client.login(username="admin", password="admin123")
        with open("blog_app/tests/images/education_blog.jpg", "rb") as image:
            response = self.client.post(
                reverse("blog_app:upload_image"), {"upload": image}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.json())
