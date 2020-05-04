from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
# from .models import Post

def index(request):
    return render(request, 'forum/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
# Create your views here.
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