from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputEmail',
                'placeholder': 'Введите логин'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputPassword1',
                'placeholder': 'Введите пароль',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputPassword1',
                'placeholder': 'Подтвердите пароль',
            }),
        } 

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', max_length=50, 
        widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputEmail',
                'placeholder': 'Введите логин'
            })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'id': 'inputPassword'
        })
    )