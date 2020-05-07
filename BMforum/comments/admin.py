from django.contrib import admin
from comments.models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object','text','created_time','user')
