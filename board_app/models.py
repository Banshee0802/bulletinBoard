from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from unidecode import unidecode
from django.urls import reverse

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег', unique=True)
    slug = models.SlugField(unique=True, editable=False, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ads_by_tag', kwargs={'tag_slug': self.slug})
    
    @property
    def ads_count(self):
        return self.ads.count()
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='ads')
    tags = models.ManyToManyField(Tag, blank=True, related_name='ads', verbose_name='Теги')
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        db_table = 'board_ads'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1

        while Advertisement.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
            unique_slug = f'{slug}-{counter}'
            counter += 1

        return unique_slug

    def __str__(self):
        return self.title
    

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    advertisement = models.ForeignKey('Advertisement', on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заявка от {self.sender} к {self.receiver} на {self.advertisement.title} - {self.status}'
    

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(unique=True, editable=False, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ads_by_category', kwargs={'category_slug': self.slug})
    
    class Meta:
        verbose_name = 'Категория объявлений'
        verbose_name_plural = 'Категории объявлений'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'advertisement']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'