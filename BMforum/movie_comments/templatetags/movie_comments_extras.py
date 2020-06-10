from django import template
from ..forms import MovieCommentForm
from ..models import MovieComment
from users.models import User
register = template.Library()
 
 
@register.inclusion_tag('movie_comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form = None):
    if form is None:
        form = MovieCommentForm()
    return {
        'form': form,
        'post': post,
    }
@register.inclusion_tag('movie_comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.moviecomment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
@register.inclusion_tag('movie_comments/inclusions/_list2.html', takes_context=True)
def show_comments_not_login(context, post):
    comment_list = post.moviecomment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
@register.inclusion_tag('movie_comments/inclusions/_likelist.html', takes_context=True)
def show_likemoviecomments(context, post):
    comment_list = MovieComment.objects.all().order_by('-like_num')[:3]
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
