from django.contrib import admin
from .models import Post, MoviePost,Category, Tag,TopicPost
 
admin.site.register(Post)
admin.site.register(MoviePost)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(TopicPost)