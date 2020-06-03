from django.contrib import admin

# Register your models here.

from .models import MovieComment
 
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ['title','name', 'post', 'created_time']
    fields = ['title','name', 'text', 'post']
    
admin.site.register(MovieComment, MovieCommentAdmin)
