from django.contrib import admin
from .models import Category,Comment, PostCategory, Post, Author

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
