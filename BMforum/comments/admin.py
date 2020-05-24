from django.contrib import admin

# Register your models here.

from .models import Comment,MovieComment
 
 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_time']
    fields = ['name', 'text', 'post']
 
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'created_time']
    fields = ['name', 'text', 'movie']

admin.site.register(Comment, CommentAdmin)
admin.site.register(MovieComment, MovieCommentAdmin)
