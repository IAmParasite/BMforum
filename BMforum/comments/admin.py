from django.contrib import admin

# Register your models here.

from .models import Comment, Like, Dislike
 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_time']
    fields = ['name', 'text', 'post']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(DisLike)
