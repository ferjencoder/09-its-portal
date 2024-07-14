# communications_app/forms.py


from django import forms
from .models import ContactMessage, QuoteRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ["name", "phone", "email", "company", "service", "message"]
