# blog_app/forms.py

from django import forms
from blog_app.models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogPostForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"),
        # widget=CKEditor5Widget(
        #    config_name="extends"
        # ),  # Usando CKEditor para el campo body
        # o
        # widget=CKEditor5Widget(config_name="id_body_name"),
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
