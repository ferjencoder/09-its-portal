# main/forms.py
# This file is used to create forms using Django's form classes. It's where forms are defined for the models or custom forms.

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


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


# Formulario de registro que incluye rol y email
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # IDEA: Agregar user a las choices si alguna vez decido implementarlo para los msjs
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
        if commit:
            user.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            Profile.objects.get_or_create(user=user, defaults={"role": role})
        return user


# Formulario para editar el usuario
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
