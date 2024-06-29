# messages_app/forms.py


from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["recipient", "content"]
