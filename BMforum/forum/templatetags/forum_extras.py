from django import template
from ..models import Post, MoviePost, Group, TopicPost

register = template.Library()

@register.inclusion_tag('forum/inclusions/_book_posts.html', takes_context=True)
def show_book_posts(context, num=5):
    return {
        'book_post_list': Post.objects.all().order_by('-views')[:num],
    }

@register.inclusion_tag('forum/inclusions/_movie_posts.html', takes_context=True)
def show_movie_posts(context, num=5):
    return {
        'movie_post_list': MoviePost.objects.all().order_by('-views')[:num],
    }

@register.inclusion_tag('forum/inclusions/_groups.html', takes_context=True)
def show_groups(context, num=5):
    return {
        'groups_list': Group.objects.all().order_by('-views')[:num],
    }

@register.inclusion_tag('forum/inclusions/_topic_posts.html', takes_context=True)
def show_topic_posts(context, num=5):
    return {
        'topic_post_list': TopicPost.objects.all().order_by('-views')[:num],
    }