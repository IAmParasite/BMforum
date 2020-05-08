from django.shortcuts import render, get_object_or_404, redirect,HttpResponse,render_to_response
from forum.models import Post
from users.models import User
from .models import Comment,CommentReply
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import datetime
import json
from django.urls import reverse
# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER','/')
    #数据检查
    user=request.user
    if not user.is_authenticated:
        return render(request,'error.html',{'message':'用户未登录','redirect_to':referer})
    text=request.POST.get('text','').strip()
    if text=='':
        return render(request,'error.html',{'message':'评论内容为空','redirect_to':referer})
    try:
        content_type=request.POST.get('content_type','')
        object_id=int(request.POST.get('object_id',''))
        model_class=ContentType.objects.get(model=content_type).model_class()
        model_obj=model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request,'error.html',{'message':'评论对象不存在','redirect_to':referer})
    #检查通过保存数据
    comment=Comment()
    comment.user=user
    comment.text=text
    comment.content_object=model_obj
    comment.save()
    return redirect(referer)

@login_required
def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)
    context = {}
    read_cookie_key=read_statistic_one_read(request,post)
    post_content_type=ContentType.objects.get_for_model(post)
    comments=Comment.objects.filter(content_type=blog_content_type,objects_id=post.pk)
    context['previous_post']=Post.objects.filter(create_time_gt=post.created_time).last()
    context['next_blog']=Blog.objects.filter(created_time_lt=post_created_time).first()
    context['post']=post
    context['comments']=comments
    response = render(request,'templates/base.html',context)
    response.set_cookie(read_cookie_key,'true')
    return response
    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
   

def reply(request,com_pk):      # 评论回复逻辑：ajax请求评论的作者和内容，完了存入数据库，再渲染页面
    if request.is_ajax():
        content = request.POST.getlist('content')
        replay_user = request.POST.getlist('user')
        re_id = User.objects.filter(username = replay_user)
        replay_time = datetime.datetime.today()
        author = request.user
        author1 = author.id
        comment = Comment.objects.get(id=com_pk)
        # print(content, replay_user, replay_time, author,comment,author1)
        if content:
            CommentReply.objects.create(content=content,comment_id=com_pk,author_id=author1,replay_user_id=author1,replay_time=replay_time)
            return HttpResponse(json.dumps({'content':content}))
    else:
        reply_list = CommentReply.objects.all()
        return render_to_response('posts/detail3.html',{ 'reply_list':reply_list},content_type="application/json")


def new_comment(request):           # 最新评论逻辑：当前登录的作者，找到他所发布的所有帖子，再遍历每篇帖子，
    newcomment_list =[]              # 找到帖子下所有的评论，再截取最前面的评论，放到一个列表，再遍历列表，显示最前面的
    userid = request.user
    userid = 3
    post_list = Post.objects.filter(author = userid)
    for post in post_list:
        comm_list = post.comment_set.all()
        num = len(comm_list)
        print('-----------------------------------------------------num',num)
        if num ==0:
            pass
        else:
            newcomment_list.append(post[:-1])
    print('------------------------------------newcomment_list',newcomment_list)

    return render(request,'posts/index.html',newcomment_list)
