from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model as user_model
User = user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
 
class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

 
class Post(models.Model):
 
    # 文章标题
    title = models.CharField('书名', max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('forum:book_detail', kwargs={'pk': self.pk})

class MoviePost(models.Model):
    title = models.CharField('影视', max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    class Meta:
        verbose_name = '影视'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('forum:movie_detail', kwargs={'pk': self.pk})

def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}

