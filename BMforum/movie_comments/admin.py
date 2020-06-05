from django.contrib import admin

# Register your models here.
from .models import MovieComment, MovieLike, MovieDislike
 
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ['title','name', 'post', 'created_time']
    fields = ['title','name', 'text', 'post']
    
admin.site.register(MovieComment, MovieCommentAdmin)
admin.site.register(MovieDislike)
admin.site.register(MovieLike)

