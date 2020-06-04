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

class Group(models.Model):
    name = models.CharField(max_length=100,unique=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    members = models.ManyToManyField(User, through='MemberShip')
    class Meta:
        verbose_name = '小组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('forum:group_detail', kwargs={'pk': self.pk})
    def get_group(self):
        return reverse('forum:group_detail', kwargs={'pk': self.pk})
        
class MemberShip(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    date_join = models.DateTimeField()
    class Meta():
        verbose_name = '小组关系'

class GroupPost(models.Model):
   title = models.CharField('标题', max_length=70)
   body = models.TextField()
   created_time = models.DateTimeField('创建时间', default = timezone.now)
   modified_time = models.DateTimeField('修改时间')
   excerpt = models.CharField(max_length=200, blank=True)
   author = models.ForeignKey(User, verbose_name='作者', null = True, on_delete=models.CASCADE)
   views = models.PositiveIntegerField(default=0, editable=False)
   group = models.ForeignKey(Group, verbose_name='小组名',related_name='grouptalk',on_delete=models.CASCADE)

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
       verbose_name = '小组讨论'
       verbose_name_plural = verbose_name
       ordering = ['-created_time']
       default_permissions = ()
       permissions = (
                  ("grouppost_delete", "讨论删除权限"),)
   def __str__(self):
       return self.title
   def get_absolute_url(self):
       return reverse('forum:group_detailmore', kwargs={'pk': self.pk})


     
class Post(models.Model):
 
    # 文章标题
    title = models.CharField('标题', max_length=70)
 
    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()
 
    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
 
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)
 
    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    # 对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 
    # ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
 
    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 
    # Category 类似。
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
 
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:book_detail', kwargs={'pk': self.pk})

class MoviePost(models.Model):
    title = models.CharField('影片', max_length=70)
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

class TopicPost(models.Model):
    title = models.CharField('话题', max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField(max_length=200, blank=True)

    views = models.PositiveIntegerField(default=0, editable=False)
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '话题'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('forum:topic_detail', kwargs={'pk': self.pk})

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

