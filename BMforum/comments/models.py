from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse

class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.Post', verbose_name='文章', on_delete=models.CASCADE)
    #点赞数量
    like_num = models.IntegerField(default = 0)
    dislike_num = models.IntegerField(default = 0)

    class Meta:
        verbose_name = '书评'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

class Like(models.Model):
    """点赞"""
    comment = models.ForeignKey("Comment",  on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add = True,verbose_name='创建时间')
    def __str__(self):
        return "%s likes comment %s" % (self.user, self.comment)

class Dislike(models.Model):
    "反对"
    comment = models.ForeignKey("Comment",  on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add = True,verbose_name='创建时间')
    def __str__(self):
        return "%s likes comment %s" % (self.user, self.comment)

