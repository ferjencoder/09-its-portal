# main/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
import os


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


class ProfileForm(forms.ModelForm):
    avatars_path = "its_portal/static/assets/images/avatars"
    predefined_image = forms.ChoiceField(
        choices=[
            (f"assets/images/avatars/{image}", image)
            for image in os.listdir(avatars_path)
        ],
        required=False,
        label="Predefined Image",
    )

    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "birth_date",
            "profile_picture",
            "predefined_image",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        predefined_image = self.cleaned_data.get("predefined_image")
        if predefined_image:
            profile.profile_picture = predefined_image
        if commit:
            profile.save()
        return profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[("client", "Client"), ("employee", "Employee"), ("admin", "Admin")],
        required=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
