<<<<<<< Updated upstream
<<<<<<< Updated upstream
from django.shortcuts import render
def index(request):
    return render(request, 'forum/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
# Create your views here.
=======
=======
>>>>>>> Stashed changes
import re
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from forum.models import Post, Category
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from comments.models import Comment
from comments.forms import CommentForm
from comments.models import CommentReply
from comments.views import new_comment

def login(request):
    if request.method=='POST':
        user = authenticate(request,username=request.POST['用户名'],password=request.POST['密码'])
        if user is None:
            return render(request, 'forum/login.html',{'错误':'用户名不存在！'})
        else:
            login(request,user)
            return rerdirect('forum:index')
    else:
        return render(request,'forum/login.html')

def register(request):
    if request.method=='POST':
        rf = UserCreationForm(request.POST)
        if rf.is_valid():
            user = authenticate(username=rf.cleaned_data['username'],password=rf.cleaned_data['password'])
            login(request, user)
            return rerdirect('forum:index')
    else:
        rf=UserCreationForm()
    content = {'注册表单': rf}
    return render(request,'forum/register.html',content)
    
class IndexView(ListView):
    model = Post        ## 告诉 django 我们要取的数据库模型是class Post, 
    template_name = 'forum/index.html'
    context_object_name = 'post_list'
    #paginate_by = 10
    


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'forum/book_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=t)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
