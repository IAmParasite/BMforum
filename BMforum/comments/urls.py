from django.urls import path
from . import views
app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
    path('moviecomment/<int:movie_pk>', views.moviecomment, name='moviecomment'),
]
