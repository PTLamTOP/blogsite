from django.contrib import admin
from .models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date_posted')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title', 'author')}
    raw_id_fields = ('author',)
    date_hierarchy = 'date_posted'
    ordering = ['date_posted']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'active', 'created_on')
    list_filter = ('created_on', 'author')
    search_fields = ('article', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_on'
    ordering = ['created_on']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)











