#forum\urls.py
from django.urls import path #导入path函数
from . import views 	#从当前的目录下导入views模块

app_name = 'forum'
urlpatterns = [			#网址和处理函数的关系写在urlpatterns列表里面
    path('', views.index, name='index'),	#第一个参数是网址，第二个参数是处理函数#第三个name 为传递的参数，这个参数的值作为处理函数index的别名（我也不太懂）
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]