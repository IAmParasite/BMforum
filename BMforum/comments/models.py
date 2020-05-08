from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model as user_model
User = user_model()
class Comment(models.Model):
    
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.Post', verbose_name='文章', on_delete=models.CASCADE)
    user1 = models.ForeignKey(User,verbose_name = '用户名',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.user.username, self.text[:20])
