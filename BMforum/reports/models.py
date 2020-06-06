from django.db import models
from django.utils import timezone
from users.models import User
from django.core.validators import MinLengthValidator
class Report(models.Model):
    title=models.CharField('举报标题', default='举报标题', max_length=50)
    name = models.CharField('用户名', max_length=50)
    text = models.TextField('举报原因',validators=[MinLengthValidator(15)])
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('comments.Comment', verbose_name='评论', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '图书举报'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])