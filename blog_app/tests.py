# blog_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import BlogPost, BlogCategory
from .forms import BlogPostForm


class BlogAppTests(TestCase):

    def setUp(self):
        self.admin_user, _ = User.objects.get_or_create(username="admin1")
        self.employee_user, _ = User.objects.get_or_create(username="employee1")
        self.admin_user.set_password("admin")
        self.employee_user.set_password("employee")
        self.admin_user.groups.add(Group.objects.get_or_create(name="admin")[0])
        self.employee_user.groups.add(Group.objects.get_or_create(name="employee")[0])
        self.admin_user.save()
        self.employee_user.save()

        self.category = BlogCategory.objects.create(name="Test Category")
        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            subtitle="Test Subtitle",
            body="Test Body",
            author=self.admin_user,
            category=self.category,
        )
        self.client = Client()

    def tearDown(self):
        print("Test executed successfully")

    def test_create_category(self):
        self.client.login(username="admin1", password="admin")
        response = self.client.post(
            reverse("blog_app:create_category"), {"name": "New Category"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BlogCategory.objects.count(), 2)

    def test_create_blog_post(self):
        self.client.login(username="admin1", password="admin")
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.count(), 2)

    def test_blog_list_view(self):
        response = self.client.get(reverse("blog_app:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_blog_detail_view(self):
        response = self.client.get(
            reverse("blog_app:blog_detail", args=[self.blog_post.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_edit_blog_post(self):
        self.client.login(username="admin1", password="admin")
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
        self.assertEqual(response.status_code, 302)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, "Updated Post")

    def test_delete_blog_post(self):
        self.client.login(username="admin1", password="admin")
        response = self.client.post(
            reverse("blog_app:delete_blog_post", args=[self.blog_post.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_employee_blog_list_view(self):
        BlogPost.objects.filter(author=self.employee_user).delete()
        self.client.login(username="employee1", password="employee")
        response = self.client.get(reverse("blog_app:employee_blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blog posts found.")

    def test_admin_blog_list_view(self):
        self.client.login(username="admin1", password="admin")
        response = self.client.get(reverse("blog_app:admin_blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_upload_image(self):
        self.client.login(username="admin1", password="admin")
        with open("blog_app/tests/images/blog_image1.jpg", "rb") as image:
            response = self.client.post(
                reverse("blog_app:upload_image"), {"upload": image}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", response.json())
