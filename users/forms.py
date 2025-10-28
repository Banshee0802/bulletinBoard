from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', 
                             required=True, 
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Введите логин'
            }),
        }  

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
            self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
            self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Подтвердите пароль'
        })
        
            self.fields['password1'].help_text = ''
            self.fields['password2'].help_text = ''

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if not password1:
            return password1
            
        if len(password1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')
        
        if password1.isdigit():
            raise ValidationError('Пароль не может состоять только из цифр.')
            
        common_passwords = ['password', 'qwerty111', 'qwerty123', 'ytrewq321']
        if password1.lower() in common_passwords:
            raise ValidationError('Этот пароль слишком распространён.')
            
        return password1  

    def _post_clean(self):
        super(forms.ModelForm, self)._post_clean()   

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
            'placeholder': 'Введите email или логин'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
        })
    )


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields['username'].label = 'Email или имя пользователя'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Введите email или имя пользователя'
        })
        self.error_messages.update({
            'invalid_login': (
                'Пожалуйста, введите корректные email/имя пользователя и пароль'
                'Обратите внимание, что оба поля могут быть чувствительны к регистру'
            ),
            'inactive': 'Аккаунт не активирован. Проверьте почту для активации по ссылке'
        })