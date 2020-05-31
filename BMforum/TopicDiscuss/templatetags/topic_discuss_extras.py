from django import template
from ..forms import TopicDiscussForm

register = template.Library()


@register.inclusion_tag('TopicDiscuss/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = TopicDiscussForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('TopicDiscuss/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.topicdiscuss_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
