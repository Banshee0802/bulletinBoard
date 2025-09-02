from django.contrib import admin

from .models import Advertisement, Category, Tag

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Tag)