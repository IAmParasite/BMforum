from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
    path('like/', views.add_like, name = 'like'),
    path('dislike/', views.add_dislike, name = 'dislike'),
]
