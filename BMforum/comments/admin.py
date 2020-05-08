from django.contrib import admin

# Register your models here.

from .models import Comment
 
 
class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'user1','post', 'created_time']
    fields = ['user1','text', 'post']
 
 
admin.site.register(Comment, CommentAdmin)
