from django.contrib import admin

# Register your models here.
from .models import Comment, Like, Dislike
 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title','name', 'post', 'created_time']
    fields = ['title','name', 'text', 'post']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Dislike)
