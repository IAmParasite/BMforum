#forum\urls.py
from django.urls import path,include #导入path函数
from . import views 	#从当前的目录下导入views模块
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
urlpatterns = [			#网址和处理函数的关系写在urlpatterns列表里面
    path('', views.index, name='index'),	#第一个参数是网址，第二个参数是处理函数#第三个name 为传递的参数，这个参数的值作为处理函数index的别名（我也不太懂）
]
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from django.contrib import admin
from django.conf import settings

app_name = 'forum'
urlpatterns = [			#网址和处理函数的关系写在urlpatterns列表里面
    path('', views.IndexView.as_view(), name='index'),	#第一个参数是网址，第二个参数是处理函数#第三个name 为传递的参数，这个参数的值作为处理函数index的别名（我也不太懂）
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    #path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    #path('search/', views.search, name='search'),
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    #path('comment/(\d+)$', views.comment, name='comment'),
    path('admin/',admin.site.urls),
    #path('ckeditor',include('ckeditor_uploader.urls')),
   # path('blog/',include(''))
    path('login/',views.login,name = 'login'),
    #path('comment/',include('comment.urls'))
]
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
