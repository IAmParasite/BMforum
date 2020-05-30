from django.urls import path
from . import views
app_name = 'TopicDiscuss'
urlpatterns = [
    path('topicdiscuss/<int:post_pk>', views.comment, name='topicdiscuss'),
]
