from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'exampleInputEmail',
                'placeholder': 'Введите логин'
            }),
            'email': forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise forms.ValidationError('Username не может содержать символ @')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email или логин', 
        max_length=50, 
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