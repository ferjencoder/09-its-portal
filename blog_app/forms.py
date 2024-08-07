# blog_app/forms.py

from django import forms
from .models import BlogPost, BlogCategory
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogCategoryForm(forms.ModelForm):
    # Form para crear y editar categorías de blogs
    class Meta:
        model = BlogCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "id": "id_name"}),
        }


class BlogPostForm(forms.ModelForm):
    # Form para crear y editar publicaciones de blogs
    body = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"),
        required=False,
    )

    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "body", "image", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "id": "id_title"}),
            "subtitle": forms.TextInput(
                attrs={"class": "form-control", "id": "id_subtitle"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control text-white", "id": "id_image"}
            ),
            "category": forms.Select(
                attrs={"class": "form-control", "id": "id_category"}
            ),
        }
