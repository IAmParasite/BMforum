from django.contrib import admin
from .models import Post, Category, Tag,Group,MemberShip,GroupPost
 
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Group)
admin.site.register(MemberShip)
admin.site.register(GroupPost)
#class GroupAdmin(admin.ModelAdmin):
#  list_display = ['id','Created_Time','user_list']
#admin.site.register(Group,GroupAdmin)
