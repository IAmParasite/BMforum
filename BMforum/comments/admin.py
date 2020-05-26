from django.contrib import admin

# Register your models here.

from .models import Comment
 
 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_time']
    fields = ['name', 'text', 'post']
 
 
admin.site.register(Comment, CommentAdmin)
