# blog/forms.py

from django import forms
from .models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogPostForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditor5Widget(config_name="id_body"),
        required=False,
    )

    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "body", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "id": "id_title"}),
            "subtitle": forms.TextInput(
                attrs={"class": "form-control", "id": "id_subtitle"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "id": "id_image"}
            ),
        }
