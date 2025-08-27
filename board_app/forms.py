from django import forms
from .models import Advertisement

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'inputDefault',
                'placeholder': 'Максимальная длина 200 символов',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': "exampleTextarea",
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),  
        }
        labels = {
            'title': 'Заголовок объявления',
            'description': 'Описание'
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) > 200:
            raise forms.ValidationError('Заголовок не должен быть длиннее 200 символов')

        return title