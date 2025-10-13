from django.contrib import admin

from .models import Advertisement, Category, Tag, Comment

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)