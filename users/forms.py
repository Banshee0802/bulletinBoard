from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=50, widget=forms.TextInput(attrs={
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')