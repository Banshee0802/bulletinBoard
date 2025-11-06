from django.contrib import admin

from .models import Advertisement, Category, Tag, Comment, News

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['advertisement_title', 'is_important', 'news_type', 'pinned']
    list_filter = ['is_important', 'news_type', 'pinned']

    def advertisement_title(self, obj):
        return obj.advertisement.title
    advertisement_title.short_description = 'Заголовок'