from django.db import models
from django.utils import timezone
from users.models import User
from django.core.validators import MinLengthValidator

class TopicDiscuss(models.Model):
    title = models.CharField('标题', max_length=70, default='title')
    name = models.CharField('名字', max_length=50)
    # name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('内容',validators=[MinLengthValidator(25)])
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('forum.TopicPost', verbose_name='话题', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '话题讨论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

