from django.db import models
from forum.models import Post
from users.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from DjangoUeditor.models import UEditorField
# Create your models here.


class Comment(models.Model):
    """评论"""
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    text = models.TextField()
    
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    class Meta:
        ordering=['-created_time']

   


class CommentReply(models.Model):
    """回复"""
    content = models.TextField()
    comment = models.ForeignKey(Comment, related_name='comment_replies',on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_comment_replies', null=True, blank=True,
                               on_delete=models.SET_NULL)
    replay_user = models.ForeignKey(User, related_name='user_replied', null=True, blank=True, on_delete=models.SET_NULL)
    replay_time = models.DateTimeField()
    # review = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}->{1}'.format(self.author, self.replay_user)
