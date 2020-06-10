import re
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import GroupPost
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag,Group,MemberShip,GroupPost, MoviePost, TopicPost
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from users.models import User
from guardian.shortcuts import assign
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_users_with_perms
from guardian.shortcuts import get_objects_for_user
from django.db.models import Q
from .forms import GroupPostForm
from django.contrib.auth.decorators import login_required


def add_post(request,group_id):
    if request.user.is_authenticated:# 发帖
        #post_list = Post.objects.all().order_by('-created_time')
        group = get_object_or_404(Group, pk = group_id)
        print("先给我把组找出来！")
        print("小组名称为")
        print(group.name)
        print("小组id为")
        print(group_id)
        form = GroupPostForm(request.POST)
        # 判断request的请求方法，如果是post方法，那么就处理数据
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            post = form.save(commit = False)
            # 将评论和被评论的文章关联起来。
            post.group = group
            post.author = request.user
            print("提交的用户是：")
            print(request.user)
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            group.save()
            post.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
            return redirect(group)
     
        # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
        # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
        context = {
            'post': group,
            'form': form,
        }
        messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
        return render(request, 'comments/preview.html', context=context)
    else:
        messages.add_message(request,messages.ERROR,"还未登录,请先登录")
        return render(request,'registration/login.html',{'错误':'还未登录！'})
        

class IndexView(ListView):
    model = Post
    template_name = 'forum/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

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

def index(request):
    return render(request,'forum/index.html')

def search_index(request):
    return render(request,'forum/search_index.html')

class BooksIndexView(ListView):
    model = Post
    template_name = 'forum/books_index.html'    
    context_object_name = 'books_list'
    paginate_by = 10

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
        
        #添加为小组成员
def add_group(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(pk = pk).first()
            user_now = User.objects.filter(username=request.user.username).first()
            mm = MemberShip.objects.filter(person=user_now,group=group_now)
            if not mm:
                m1=MemberShip.objects.create(person=user_now,group=group_now,date_join=timezone.now())
            messages.add_message(request,messages.SUCCESS,"加入小组成功")
            return redirect('forum:groups_index')

        else:
            messages.add_message(request,messages.ERROR,"还未登录,请先登录")
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
##管理员添加
def add_groupmanager(request,name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(name = name).first()
            user_now = User.objects.filter(username=request.user.username).first()
            gg = GroupPost.objects.filter(group=group_now)
            if  group_now:
                for gp in gg:
                    assign_perm('grouppost_delete',user_now, gp)
            
            messages.add_message(request,messages.SUCCESS,"申请管理员成功")
            return redirect('forum:groups_index')

        else:
            messages.add_message(request,messages.ERROR,"还未登录,请先登录")
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
#删除小组内的帖子
def deleteGroupPost(request,pk,pkk):
    groupp = GroupPost.objects.get(pk=pk)
    groupp.delete()
    messages.add_message(request,messages.SUCCESS,"删除帖子成功")
    return redirect('/groups/'+str(pkk))
#置顶帖子
def topenGroupPost(request,pk,pkk):
    groupp = GroupPost.objects.get(pk=pk)
    groupp.top = True
    groupp.top_time = timezone.now()
    groupp.save()
    messages.add_message(request,messages.SUCCESS,"帖子置顶成功")
    return redirect('/groups/'+str(pkk))
def imGroupPost(request,pk,pkk):
    groupp = GroupPost.objects.get(pk=pk)
    groupp.im = True
    groupp.save()
    messages.add_message(request,messages.SUCCESS,"帖子设精华成功")
    return redirect('/groups/'+str(pkk))
class GroupsIndexView(ListView):
    model = Group        ## 告诉 django 我们要取的数据库模型是class GroupPost,
    template_name = 'forum/groups_index.html'
    context_object_name = 'groups_list'
#paginate_by = 10

class GroupPostView(ListView):
    model = GroupPost
    template_name = 'forum/group_detail.html'
    context_object_name = 'group_post'
    def get_queryset(self):
        c = Group.objects.filter(pk=self.kwargs['pk']).first()
        
        return GroupPost.objects.filter(group=c).order_by('-top_time','created_time')
        
            
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
#        md = markdown.Markdown(extensions=[
#            'markdown.extensions.extra',
#            'markdown.extensions.codehilite',
#            TocExtension(slugify=slugify),
#        ])
#        post.members = md.convert(post.members)
#        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#        post.toc = m.group(1) if m is not None else ''
        return post
        
class GroupDetailView(DetailView):
# 这些属性的含义和 ListView 是一样的
    model = GroupPost
    template_name = 'forum/group_detailmore.html'
    context_object_name = 'grouppost'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(GroupDetailView, self).get(request, *args, **kwargs)

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

class MoviesIndexView(ListView):
    model = MoviePost        ## 告诉 django 我们要取的数据库模型是class Post, 
    template_name = 'forum/movies_index.html'
    context_object_name = 'movies_list'
    #paginate_by = 10
class MoviePostDetailView(DetailView):
    model = MoviePost 
    template_name = 'forum/movie_detail.html'
    context_object_name = 'movie_post'
    def get(self, request, *args, **kwargs):
        response = super(MoviePostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post

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
class TopicIndexView(ListView):
    model = TopicPost        ## 告诉 django 我们要取的数据库模型是class Post,
    template_name = 'forum/topic_index.html'
    context_object_name = 'topics_list'
    #paginate_by = 10

        
        #添加为小组成员
def add_group(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(pk = pk).first()
            user_now = User.objects.filter(username=request.user.username).first()
            mm = MemberShip.objects.filter(person=user_now,group=group_now)
            if not mm:
                m1=MemberShip.objects.create(person=user_now,group=group_now,date_join=timezone.now())
            return redirect('forum:groups_index')

        else:
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
##管理员添加
def add_groupmanager(request,name):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            group_now  = Group.objects.filter(name = name).first()
            user_now = User.objects.filter(username=request.user.username).first()
            gg = GroupPost.objects.filter(group=group_now)
            if  group_now:
                for gp in gg:
                    assign_perm('grouppost_delete',user_now, gp)
            return redirect('forum:groups_index')

        else:
            return render(request,'registration/login.html',{'错误':'还未登录！'})
    else:
        return render(request,'forum/login.html')
        
    
class GroupsIndexView(ListView):
    model = Group        ## 告诉 django 我们要取的数据库模型是class GroupPost,
    template_name = 'forum/groups_index.html'
    context_object_name = 'groups_list'
#paginate_by = 10

class GroupPostView(ListView):
    model = GroupPost
    template_name = 'forum/group_detail.html'
    context_object_name = 'group_post'
    def get_queryset(self):
        c = Group.objects.filter(pk=self.kwargs['pk']).first()

        return GroupPost.objects.filter(group=c).order_by('created_time')
        
            
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
#        md = markdown.Markdown(extensions=[
#            'markdown.extensions.extra',
#            'markdown.extensions.codehilite',
#            TocExtension(slugify=slugify),
#        ])
#        post.members = md.convert(post.members)
#        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#        post.toc = m.group(1) if m is not None else ''
        return post
        

class GroupDetailView(DetailView):
# 这些属性的含义和 ListView 是一样的
    model = GroupPost
    template_name = 'forum/group_detailmore.html'
    context_object_name = 'grouppost'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(GroupDetailView, self).get(request, *args, **kwargs)

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

class MoviesIndexView(ListView):
    model = MoviePost        ## 告诉 django 我们要取的数据库模型是class Post, 
    template_name = 'forum/movies_index.html'
    context_object_name = 'movies_list'
    #paginate_by = 10
class MoviePostDetailView(DetailView):
    model = MoviePost 
    template_name = 'forum/movie_detail.html'
    context_object_name = 'movie_post'
    def get(self, request, *args, **kwargs):
        response = super(MoviePostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post
#class TopicIndexView(ListView):
#   model = Post        ## 告诉 django 我们要取的数据库模型是class Post, 
#  template_name = 'forum/books_index.html'
#    context_object_name = 'post_list'
#    #paginate_by = 10

#class TopicIndexView(ListView):
#   model = Post        ## 告诉 django 我们要取的数据库模型是class Post, 
#  template_name = 'forum/books_index.html'
#    context_object_name = 'post_list'
#    #paginate_by = 10
class TopicIndexView(ListView):
    model = TopicPost        ## 告诉 django 我们要取的数据库模型是class Post,
    template_name = 'forum/topic_index.html'
    context_object_name = 'topic_list'
    #paginate_by = 10
class TopicPostDetailView(DetailView):
    model = TopicPost
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic_post'
    def get(self, request, *args, **kwargs):
        response = super(TopicPostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post

class TopicPostDetailView(DetailView):
    model = TopicPost
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic_post'
    def get(self, request, *args, **kwargs):
        response = super(TopicPostDetailView, self).get(request, *args, **kwargs)
        # self.object.increase_views()
        return response
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
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
        return redirect('forum:index')

    book_post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    movie_post_list = MoviePost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    groups_list = Group.objects.filter(Q(name__icontains=q))
    topic_post_list = TopicPost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'forum/search_index.html', {'book_post_list': book_post_list,
                                                        'movie_post_list':movie_post_list,
                                                        'groups_list': groups_list,
                                                        'topic_post_list': topic_post_list})

def book_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('forum:books_index')

    books_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    
    return render(request, 'forum/books_index.html', {'books_list': books_list})

def movie_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('forum:movies_index')

    movies_list = MoviePost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'forum/movies_index.html', {'movies_list': movies_list})

def group_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('forum:groups_index')

    groups_list = Group.objects.filter(Q(name__icontains=q))
    return render(request, 'forum/groups_index.html', {'groups_list': groups_list})

def group_post_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('forum:group_detail')

    group_post = GroupPost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'forum/group_detail.html', {'group_post': group_post})

def topic_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('forum:topic_index')

    topics_list = TopicPost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'forum/topic_index.html', {'topics_list': topics_list})

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
