# main/forms.py

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.utils.translation import gettext_lazy as _


# Formulario para registro de usuarios
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        if len(cd["password1"]) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return cd["password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username


# Formulario para actualizar perfil de usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date", "profile_picture"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[
            ("client", "Client"),
            ("employee", "Employee"),
            ("admin", "Admin"),
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "role",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        role = self.cleaned_data["role"]
        print(f"Form: Saving user with role {role}")
        if commit:
            user.save()
            print(f"User saved with role: {role}")
            group = Group.objects.get(name=role)
            user.groups.add(group)
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.role = role
                profile.save()
                print(f"Form: Profile saved with role {profile.role}")
        return user


# Formulario para editar el usuario
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
