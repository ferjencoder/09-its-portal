# blog/models.py

import os
import re
from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = CKEditor5Field("Body", config_name="extends")  # Usando CKEditor para el body
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Eliminar imagen principal del post
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        # Buscar y eliminar imágenes dentro del contenido del body
        img_tags = re.findall(r'<img.*?src="(.*?)"', self.body)
        for img_path in img_tags:
            # Convertir ruta relativa a absoluta
            full_path = os.path.join(settings.BASE_DIR, img_path.lstrip("/"))
            if os.path.isfile(full_path):
                os.remove(full_path)

        super(BlogPost, self).delete(*args, **kwargs)
