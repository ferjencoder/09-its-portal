# blog_app/models.py

import os
import re
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"  # Corrección del nombre plural


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = CKEditor5Field("Body", config_name="extends")  # Usando CKEditor para el body
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Añadir campo updated_at
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, related_name="posts"
    )

    def delete(self, *args, **kwargs):
        # Eliminar imagen principal del post
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        # Buscar y eliminar imágenes dentro del contenido del body
        img_tags = re.findall(r'<img.*?src="([^"]+)"', self.body)
        if not img_tags:
            img_tags = re.findall(r"<img.*?src=\'([^\']+)\'", self.body)
        if not img_tags:
            img_tags = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', self.body)

        for img_path in img_tags:
            if img_path.startswith("/media/"):
                img_path = img_path[len("/media/") :]
            full_path = os.path.join(settings.MEDIA_ROOT, img_path)
            if os.path.isfile(full_path):
                os.remove(full_path)

        super(BlogPost, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title
