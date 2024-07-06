# blog_app/models.py

import os
import re
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = CKEditor5Field("Body", config_name="extends")  # Usando CKEditor para el body
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )

    def delete(self, *args, **kwargs):
        # Eliminar imagen principal del post
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
            # print(f"Deleted main image: {self.image.path}")  # Mensaje de depuración

        # Ver contenido del cuerpo del blog
        # print(f"Blog post body content: {self.body}")

        # Buscar y eliminar imágenes dentro del contenido del body
        img_tags = re.findall(r'<img.*?src="([^"]+)"', self.body)
        if not img_tags:
            img_tags = re.findall(r"<img.*?src=\'([^\']+)\'", self.body)
        if not img_tags:
            img_tags = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', self.body)

        # print(
        #    f"Found images: {img_tags}"
        # )  # Mensaje de depuración para las imágenes encontradas
        for img_path in img_tags:
            # Eliminar el prefijo '/media/' si existe en la ruta
            if img_path.startswith("/media/"):
                img_path = img_path[len("/media/") :]
            full_path = os.path.join(settings.MEDIA_ROOT, img_path)
            # print(
            #    f"Full path to delete: {full_path}"
            # )  # Mensaje de depuración para la ruta completa
            if os.path.isfile(full_path):
                os.remove(full_path)
                # print(f"Deleted embedded image: {full_path}")  # Mensaje de depuración

        # Llamar al método delete de la clase padre
        super(BlogPost, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title
