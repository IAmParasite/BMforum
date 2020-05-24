from django.contrib import admin
from .models import Post, MoviePost,Category, Tag
 
admin.site.register(Post)
admin.site.register(MoviePost)
admin.site.register(Category)
admin.site.register(Tag)