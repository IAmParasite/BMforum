from django.conf.urls import url
from django.urls import path
from .views import post_comment,reply
from . import views

app_name = 'comments'

urlpatterns = [
    path('update_comment',views.update_comment,name='update_comment')
]
