from django.contrib import admin
from .models import Post, Category, Tag, Group ,MemberShip, GroupPost, MoviePost, TopicPost
 
admin.site.register(Post)
admin.site.register(MoviePost)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Group)
admin.site.register(MemberShip)
admin.site.register(GroupPost)
admin.site.register(TopicPost)

 





