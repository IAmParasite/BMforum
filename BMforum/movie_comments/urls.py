from django.urls import path
from . import views
app_name = 'movie_comments'
urlpatterns = [
    path('movie_comment/<int:post_pk>', views.comment, name='movie_comment'),
]
