from django.db import models
from django.utils import timezone
from users.models import User
 
class MovieComment(models.Model):
    title = models.CharField('标题', max_length=70, default='title')
    name = models.CharField('名字', max_length=50)
    #name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.MoviePost', verbose_name='文章', on_delete=models.CASCADE)
    like_num = models.IntegerField(default = 0)
    dislike_num = models.IntegerField(default = 0)

    class Meta:
        verbose_name = '影评'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

class MovieLike(models.Model):
    comment = models.ForeignKey("MovieComment",  on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now_add = True,verbose_name='创建时间')
    def __str__(self):
        return "%s likes comment %s" % (self.user, self.comment)

class MovieDislike(models.Model):
    comment = models.ForeignKey("MovieComment",  on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = '创建时间')
    def __str__(self):
        return "%s likes comment %s" % (self.user, self.comment)



