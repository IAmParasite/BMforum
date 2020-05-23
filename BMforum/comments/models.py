from django.db import models
from django.utils import timezone
from users.models import User
 
class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    #name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.Post', verbose_name='文章', on_delete=models.CASCADE)
 
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
class MovieComment(models.Model):
    name = models.CharField('名字', max_length=50)
    #name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.MoviePost', verbose_name='文章', on_delete=models.CASCADE)
 
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

