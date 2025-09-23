from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from users.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=63,
        required=True,
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}),
        label="Username",
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")

