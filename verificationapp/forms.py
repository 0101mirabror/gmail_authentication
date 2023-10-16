# appname/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


from django.contrib.auth.password_validation import validate_password
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
             
        )
    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    