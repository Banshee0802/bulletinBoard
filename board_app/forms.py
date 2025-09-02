from django import forms
from .models import Advertisement, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название тега',
            }),
        }
    labels = {
        'name': 'Название тега',
    }


class AdvertisementForm(forms.ModelForm):

    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новые теги через запятую'
        }),
        label='Новые теги'
    )

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
    

    def save(self, commit=True):
        advertisement = super().save(commit=False)
        
        if commit:
            advertisement.save()
            self.save_m2m() 
            
            new_tags = self.cleaned_data.get('new_tags', '')
            if new_tags:
                tag_names = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    advertisement.tags.add(tag)
        
        return advertisement