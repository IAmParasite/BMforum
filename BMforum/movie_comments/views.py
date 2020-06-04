from forum.models import MoviePost
from .models import MovieComment, MovieDislike, MovieLike
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.decorators.http import require_POST
from .forms import MovieCommentForm
from django.contrib import messages
import json
import datetime
import markdown

@require_POST
def comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(MoviePost, pk=post_pk)
 
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = MovieCommentForm(request.POST)
 
    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        print(comment)
        
        # 将评论和被评论的文章关联起来。
        comment.post = post
        comment.name = request.user
        comment.text = markdown.markdown(comment.text,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
        # 最终将评论数据保存进数据库，调用模型实例的 save 方法
        comment.save()
        post.save()
        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect(post)
 
    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'movie_comments/preview.html', context=context)

def add_like(request):
    if request.is_ajax():
        user = request.user
        print(user)
        contentid = request.POST.getlist('contend_id')
        Commentt = MovieComment.objects.get(id = contentid[0])
        created_time = datetime.datetime.now()
        comment_id = MovieLike.objects.filter(comment_id = Commentt, user_id = request.user.id)
        if comment_id.exists():
            resp = {'status': '已经点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            Commentt.like_num +=1
            Commentt.save()
            MovieLike.objects.update_or_create(user = user, comment = Commentt, created_time = created_time)
            resp = {'errorcode': 100, 'status': '成功点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

def add_dislike(request):
    print("dislike")
    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')
        # contentid = request.POST.get('contend_id')
        Commentt = MovieComment.objects.get(id = contentid[0])
        created_time = datetime.datetime.now()
        comment_id = MovieDislike.objects.filter(comment_id = Commentt, user_id = request.user.id)
        if comment_id.exists():
            resp = {'status': '已经反对'}
            return HttpResponse(json.dumps(resp), content_type = "application/json")
        else:
            Commentt.dislike_num += 1
            Commentt.save()
            MovieDislike.objects.update_or_create(user = user, comment = Commentt, created_time = created_time)
            resp = {'errorcode': 100, 'status': '成功反对'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
