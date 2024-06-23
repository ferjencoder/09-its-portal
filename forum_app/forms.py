# forum_app/forms.py

from django import forms
from .models import ForumTopic, ForumPost


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
