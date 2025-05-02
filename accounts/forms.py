#Register validation form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if len(re.findall(r"\d", password)) < 3:
            raise ValidationError("Password must include at least 3 numbers.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError("Password must include at least 1 special character.")

        return password