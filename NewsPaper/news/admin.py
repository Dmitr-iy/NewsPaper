from django.contrib import admin
from .models import Category, Comment, PostCategory, Post, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'dateTime', 'newsArticle')
    list_filter = ('category', 'dateTime')
    search_fields = ('author', 'newsArticle')

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
