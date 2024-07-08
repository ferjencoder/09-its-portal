# forum_app/forms.py

from django import forms
from .models import ForumTopic, ForumPost


class ForumTopicForm(forms.ModelForm):
    # Formulario para crear y editar temas del foro
    class Meta:
        model = ForumTopic
        fields = ["title", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class ForumPostForm(forms.ModelForm):
    # Formulario para crear y editar publicaciones del foro
    class Meta:
        model = ForumPost
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
